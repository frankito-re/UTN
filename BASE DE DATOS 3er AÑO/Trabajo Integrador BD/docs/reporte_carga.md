# Reporte de carga masiva · Bodegas del Atuel

Generado el 2026-11-10 con `db/seed/cargar_datos.py` (escala **1.0**, semilla **42**, fecha de referencia 2026-11-10; con `--fecha-ref hoy` las ventanas «última semana/mes» quedan relativas al día de la ejecución). Misma semilla y escala producen los mismos datos.

Reproducir exactamente esta carga: `.venv/bin/python db/seed/cargar_datos.py --limpiar --escala 1.0 --semilla 42 --fecha-ref 2026-11-10` (requiere el contenedor levantado y `pip install -r db/seed/requirements.txt` en un entorno virtual).

**Tiempo total:** 15.1 s · **Tamaño de la base:** 105 MB

## Conteos por tabla

| Tabla | Filas |
| :-- | --: |
| `localidad` | 39 |
| `sala_venta` | 40 |
| `empleado` | 400 |
| `finca` | 100 |
| `cepa` | 12 |
| `bodega` | 25 |
| `parcela` | 1,400 |
| `lote_uva` | 13,640 |
| `analisis_calidad` | 27,241 |
| `vino` | 600 |
| `composicion` | 1,201 |
| `maridaje` | 8 |
| `vino_maridaje` | 1,177 |
| `cliente` | 20,000 |
| `socio` | 18,000 |
| `distribuidor` | 1,000 |
| `exportador` | 1,000 |
| `permiso_exportacion` | 2,655 |
| `transportista` | 15 |
| `cobertura_transportista` | 136 |
| `comprobante` | 160,000 |
| `renglon_comprobante` | 507,134 |
| `ingreso` | 289 |
| `renglon_ingreso` | 1,411 |
| `transferencia` | 5,490 |
| `renglon_transferencia` | 35,127 |
| `stock_sala` | 19,972 |
| `stock_deposito` | 600 |
| `auditoria_precio` | 1,020 |

Cumple el requisito del TP: al menos una tabla con más de 100.000 filas (`renglon_comprobante`: 507,134) y tres o más con más de 10.000 (`lote_uva`, `analisis_calidad`, `cliente`, `socio`, `comprobante`, `renglon_comprobante`, `renglon_transferencia`, `stock_sala`).

## Tiempos por fase

| Fase | Segundos |
| :-- | --: |
| Generacion en memoria | 3.89 |
| Truncate y triggers de carga apagados | 0.07 |
| COPY localidad (39 filas) | 0.00 |
| COPY sala_venta (40 filas) | 0.00 |
| COPY empleado (400 filas) | 0.00 |
| COPY finca (100 filas) | 0.00 |
| COPY cepa (12 filas) | 0.00 |
| COPY bodega (25 filas) | 0.00 |
| COPY parcela (1,400 filas) | 0.02 |
| COPY lote_uva (13,640 filas) | 0.18 |
| COPY analisis_calidad (27,241 filas) | 0.15 |
| COPY vino (600 filas) | 0.01 |
| COPY composicion (1,201 filas) | 0.01 |
| COPY maridaje (8 filas) | 0.00 |
| COPY vino_maridaje (1,177 filas) | 0.02 |
| COPY cliente (20,000 filas) | 0.30 |
| COPY socio (18,000 filas) | 0.13 |
| COPY distribuidor (1,000 filas) | 0.01 |
| COPY exportador (1,000 filas) | 0.01 |
| COPY permiso_exportacion (2,655 filas) | 0.02 |
| COPY transportista (15 filas) | 0.00 |
| COPY cobertura_transportista (136 filas) | 0.00 |
| COPY comprobante (160,000 filas) | 2.14 |
| COPY renglon_comprobante (507,134 filas) | 5.53 |
| COPY ingreso (289 filas) | 0.01 |
| COPY renglon_ingreso (1,411 filas) | 0.02 |
| COPY transferencia (5,490 filas) | 0.03 |
| COPY renglon_transferencia (35,127 filas) | 0.34 |
| COPY stock_sala (19,972 filas) | 0.18 |
| COPY stock_deposito (600 filas) | 0.01 |
| Triggers reactivados y secuencias ajustadas | 0.01 |
| COMMIT (validacion de triggers diferidos) | 0.25 |
| VACUUM (ANALYZE) | 0.56 |
| Ajustes de precio (generan auditoria por trigger) | 0.04 |
| REFRESH de la vista materializada | 0.47 |
| OK  Comprobantes cuyo total no coincide con  | 0.24 |
| OK  Renglones cuyo subtotal no coincide con  | 0.19 |
| OK  Comprobantes con distinto resultado que  | 0.01 |
| OK  Stock de sala distinto de transferido -  | 0.09 |
| OK  Stock de deposito distinto de ingresado  | 0.01 |
| OK  Vinos cuyo corte no suma 100 | 0.00 |
| OK  Clientes sin fila en su subtipo | 0.02 |
| OK  Triggers que quedaron desactivados | 0.00 |

## Verificaciones de coherencia

| Verificación | Inconsistencias |
| :-- | --: |
| Comprobantes cuyo total no coincide con la suma de sus renglones | 0 |
| Renglones cuyo subtotal no coincide con fn_subtotal_renglon | 0 |
| Comprobantes con distinto resultado que fn_calcular_comprobante (muestra de 3000) | 0 |
| Stock de sala distinto de transferido - vendido | 0 |
| Stock de deposito distinto de ingresado - transferido | 0 |
| Vinos cuyo corte no suma 100 | 0 |
| Clientes sin fila en su subtipo | 0 |
| Triggers que quedaron desactivados | 0 |

La auditoría de precios (`auditoria_precio`) no se carga: la generan los triggers al aplicar tres rondas de ajuste de precios después de la carga.
