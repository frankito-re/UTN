# Informe de índices y rendimiento · Bodegas del Atuel (Etapa 4)

Índices en [`db/migrations/008_indices.sql`](../db/migrations/008_indices.sql). Medición con
[`db/tests/medir_rendimiento.py`](../db/tests/medir_rendimiento.py). Planes completos antes y después en
[`docs/rendimiento/resultados.md`](rendimiento/resultados.md); datos crudos en `docs/rendimiento/*.json`.

## 1. Metodología

- **Datos:** carga de la Etapa 3 (escala 1.0): 160.000 comprobantes, 507.134 renglones, 20.000 clientes, 6.776 transferencias.
- **Estado «antes»:** solo las PK y los `UNIQUE` de `001`/`002` (40 índices). PostgreSQL **no** indexa las columnas de FK.
- **Procedimiento:** `VACUUM (ANALYZE)`; por consulta se descarta la primera ejecución y se toma la **mediana de 7**
  con `EXPLAIN (ANALYZE, BUFFERS)`. Los datos (80 MB) caben en `shared_buffers`: son tiempos **con cache caliente**.
  Los *bloques* (buffers) tocados no dependen del cache y muestran el trabajo real.
- **Tres estados:** *Antes* (sin índices) → *Solo índices* (15 índices de 008, planificador por defecto) →
  *Después* (índices + `random_page_cost = 1.1`). Separarlos evita atribuir a un índice lo que hizo un parámetro.
- Las consultas son las de la Etapa 5 (S1, S3, S4, S5, S8), más la ficha de cliente, el autocompletado y el borrado de un vino (RN-14).

## 2. Resultados

| Consulta | Antes (ms) | Solo índices (ms) | Después (ms) | Mejora | Bloques antes → después |
| :-- | --: | --: | --: | --: | --: |
| **Q1** Ventas por sala del último trimestre (S8) | 8.34 | 2.34 | 2.00 | 4.2× | 1.346 → 141 |
| **Q2** Últimas 20 compras de un cliente | 6.18 | 0.03 | 0.02 | 294× | 1.334 → 23 |
| **Q3** Unidades vendidas de un vino por mes | 27.46 | 25.88 | 3.81 | 7.2× | 5.114 → 7.907 |
| **Q4** Top 10 vinos más vendidos (S1) | 67.22 | 72.26 | 71.69 | 0.9× (sin mejora) | 3.809 → 3.809 |
| **Q5** Clientes por tipo en una sala, última semana (S3) | 5.60 | 0.06 | 0.04 | 147× | 1.365 → 37 |
| **Q6** Transferencias pendientes por sala (S5) | 0.26 | 0.06 | 0.05 | 5.3× | 30 → 2 |
| **Q7** Autocompletado de clientes por nombre | 6.98 | 1.30 | 1.14 | 6.1× | 275 → 272 |
| **Q8** Salas con más pedidos de un vino, 15 días (S4) | 1.55 | 0.35 | 0.10 | 15× | 220 → 201 |
| **Q9** Borrar un vino sin movimientos (FK, RN-14) | 22.51 | 0.17 | 0.28 | 79× | 5 → 5 |
| **Q10** Ventas de toda la red, último trimestre | 6.72 | 1.53 | 1.47 | 4.6× | 1.334 → 72 |

## 3. Qué índice resuelve qué (y qué plan cambió)

| Tipo | Índice | Consulta | Cambio de plan |
| :-- | :-- | :-- | :-- |
| **Compuesto** | `idx_comprobante_cliente_fecha (id_cliente, fecha DESC)` | Q2, FK de `comprobante.id_cliente` | `Seq Scan` + `Sort` → `Index Scan` sin ordenar: el `LIMIT 20` corta a las 20 primeras filas. |
| **Compuesto + INCLUDE** | `idx_comprobante_sala_fecha (id_sala, fecha) INCLUDE (total)` | Q1, Q5, FK de `id_sala` | Q1 pasa a `Index Only Scan`: suma `total` sin leer la tabla. |
| **Compuesto + INCLUDE** | `idx_renglon_transferencia_vino (cod_vino, nro_transferencia) INCLUDE (cantidad)` | Q8 | `Seq Scan` de 43.000 renglones → `Index Only Scan`. |
| **INCLUDE (covering)** | `idx_renglon_comprobante_vino (cod_vino) INCLUDE (cantidad)` | Q3, Q9 | Q3: de recorrer 507.000 renglones a buscar los ~1.600 de un vino. Q9: ver §4. |
| **BRIN** | `brin_comprobante_fecha (fecha)` | Q10 | `Parallel Seq Scan` (1.334 bloques) → `Bitmap Heap Scan` por BRIN (72 bloques). |
| **Parcial** | `idx_transferencia_pendientes (id_sala) WHERE estado <> 'procesado'` | Q6 | `Seq Scan` → `Index Only Scan` sobre 2 bloques: el índice solo contiene las ~200 pendientes de 6.776. |
| **De expresión** | `idx_cliente_nombre_lower (lower(nombre_razon_social) text_pattern_ops)` | Q7 | `Seq Scan` de 20.000 clientes → `Bitmap Index Scan`; sin el índice, `lower(...)` impide usar cualquier índice común. |
| **FK (RN-14)** | `idx_renglon_ingreso_vino`, `idx_stock_sala_vino`, `idx_auditoria_precio_vino`, `idx_ingreso_transportista_fecha`, `idx_ingreso_bodega`, `idx_vino_bodega`, `idx_lote_uva_bodega`, `idx_empleado_sala` | Q9 y los borrados de transportista, bodega, sala | Verificación de FK por índice en lugar de recorrer la tabla hija. |

**Por qué BRIN y no B-tree en `comprobante.fecha`:** los comprobantes se insertan en orden cronológico, así que la fecha
está ordenada físicamente. Medí un B-tree sobre la misma columna: Q10 tarda lo mismo (1.4 ms contra 1.5 ms) pero ocupa
**1.112 kB contra 24 kB** (46 veces más) y cuesta más en cada `INSERT`. BRIN pierde cuando los datos no están ordenados
físicamente (por ejemplo, tras muchos `UPDATE`/`DELETE` que reubiquen filas): en ese caso habría que `CLUSTER` o pasar a B-tree.

## 4. Hallazgos que no eran obvios

1. **Q9: la FK sin índice cuesta (RN-14).** Borrar un vino que no tiene movimientos tardaba **22.5 ms**: la base verifica
   la restricción contra cada tabla hija y, sin índice en `renglon_comprobante.cod_vino`, recorre las 507.000 filas
   (`Trigger for constraint renglon_comprobante_cod_vino_fkey: time=20.840`). Con el índice, esa verificación baja a
   **0.040 ms**. Es el argumento principal para indexar las FK que `ON DELETE RESTRICT` obliga a comprobar.
2. **Q3: el índice solo no alcanzó; hizo falta `random_page_cost`.** Con el índice y la configuración por defecto
   el tiempo casi no cambió (27.5 → 25.9 ms) porque el planificador seguía eligiendo un `Seq Scan` de los 160.000
   comprobantes: con `random_page_cost = 4.0` (valor pensado para discos giratorios) estima caro hacer 1.600 búsquedas
   por PK. Con `1.1` (SSD, base en cache) elige `Nested Loop` con búsquedas por PK y baja a **3.8 ms**. Por eso `008`
   fija `ALTER DATABASE ... SET random_page_cost = 1.1`. El número de bloques sube (5.114 → 7.907) porque cada búsqueda por
   PK toca varias páginas de índice, pero son *hits* de cache y la consulta es 7 veces más rápida.
3. **Q4: ningún índice ayuda y se dejó tal cual.** El ranking global agrega **todos** los renglones: leerlos por
   índice (`Index Only Scan`, que se puede forzar con `enable_seqscan = off`) tarda lo mismo que el `Seq Scan` paralelo
   (≈ 65 ms). Una consulta que siempre recorre el 100 % de la tabla no se acelera con índices; se resuelve con un
   resumen precalculado (una vista materializada de ventas por vino, como `mv_ventas_mensuales_sala`) si el tablero la pide
   con frecuencia. No se agregó para no crecer el alcance de la Etapa 4; queda como mejora.
4. **Q1: el planificador no usó el BRIN.** Con el filtro por fecha y el `JOIN` a sala eligió `idx_comprobante_sala_fecha`
   (index-only). El BRIN gana cuando la consulta no filtra por sala (Q10), que es el caso del tablero de red.

## 5. Costo de escritura

Cada índice se actualiza en cada `INSERT`, `UPDATE` y `DELETE` de su tabla.

| Medida | Sin índices | Con los 15 índices | Sobrecosto |
| :-- | --: | --: | --: |
| Registrar una venta (comprobante + 3 renglones, con todos los triggers de venta), ms | 0.749 | 0.901 | **+20 %** |
| Carga masiva: `COPY comprobante` (160.000 filas) | 1.59 s | 2.14 s | +35 % |
| Carga masiva: `COPY renglon_comprobante` (507.134 filas) | 4.65 s | 5.64 s | +21 % |
| Carga masiva completa | 13.6 s | 15.5 s | +14 % |
| Tamaño de la base | 85.5 MB | 112.6 MB | +27.1 MB (+32 %) |

- Un sobrecosto de +20 % por venta (0.15 ms) es despreciable frente al beneficio en lectura: las consultas de ficha
  y tablero pasaron de milisegundos a centésimas de milisegundo.
- Los tres índices grandes (`idx_renglon_comprobante_vino` 12.9 MB, `idx_comprobante_sala_fecha` 7.1 MB,
  `idx_comprobante_cliente_fecha` 4.7 MB) son el 90 % del espacio; el BRIN ocupa 24 kB.
- Para cargas masivas conviene **crear los índices después del `COPY`**: el script de carga mide ~14 % más con
  los índices ya creados.
- **No se indexó todo:** las FK de tablas chicas o que nunca se borran (`sala_venta.cod_postal`, `cliente.cod_postal`,
  `parcela.id_cepa`, …) quedaron sin índice a propósito; su costo de escritura no tiene contrapartida medida.

## 6. Cómo reproducir

```bash
docker compose down -v && docker compose up -d                       # crea la base con 001..008
.venv/bin/python db/seed/cargar_datos.py --limpiar                   # carga masiva
.venv/bin/python db/tests/medir_rendimiento.py despues               # mide con los índices
# Para el «antes»: eliminar los índices de 008 (DROP INDEX ...), medir con «antes», volver a crearlos.
.venv/bin/python db/tests/medir_rendimiento.py comparar              # regenera resultados.md
```

Las mediciones dependen de la máquina; lo reproducible es el **orden de magnitud** y el **cambio de plan**.
