# Front · Bodegas del Atuel

HTML + JavaScript (módulos ES) **sin dependencias ni paso de compilación**, servido por nginx.
Habla con la API por `/api` (mismo origen: nginx hace de proxy, no hace falta CORS).

```bash
docker compose up -d --build     # base + API + front
open http://localhost:8080
```

## Pantallas

| Ruta | Qué hace |
| :-- | :-- |
| `#/vinos` | Catálogo paginado con filtros (nombre, tipo, bodega, precio, stock, orden) |
| `#/vinos/nuevo`, `#/vinos/{id}/editar` | Alta y edición de un vino con su corte y maridajes |
| `#/vinos/{id}` | Ficha: datos, corte, maridajes, stock e historial de precios (RN-13); baja |
| `#/ventas`, `#/ventas/nueva`, `#/ventas/{n}` | Listado, nueva venta (cliente + sala + vinos) y comprobante |
| `#/transferencias…`, `#/ingresos…` | Ciclo de vida: crear en confección → terminar → procesar (mueve stock) |
| `#/tablero` | Vinos más vendidos, ventas mensuales por sala, stock crítico, refresco de la vista materializada |

## Reglas de diseño

* **Sin lógica de cálculo en el cliente.** La venta solo envía cliente, sala, vinos y cantidades; precios,
  descuento, subtotales, total y stock los calcula la base y se muestran tal cual llegan. Un test estático
  (`test/seguridad_estatica.test.mjs`) falla si las vistas suman con `reduce` o multiplican precios.
* **Errores de negocio visibles.** El cuerpo de error de la API (`mensaje`, `regla`, `detalle`) se muestra en un
  cartel: «Conflicto · RN-09 — Stock insuficiente…», «RN-05 — el corte suma 90…», etc.
* **Sin XSS.** Los datos se insertan como nodos de texto, nunca como HTML (`ui.js`); la CSP de nginx no permite
  scripts ni estilos en línea. Los tests verifican que no se use `innerHTML` ni equivalentes.
* Responsive y con modo oscuro (`prefers-color-scheme`).

## Pruebas

```bash
node --test "front/test/*.test.mjs"      # 9 pruebas: utilidades puras y controles estáticos de seguridad
```

Además se verificó en un navegador real, de punta a punta: venta exitosa (comprobante calculado por la base) y
rechazada por RN-09, alta con corte que no suma 100 (RN-05) y luego correcta, cambio de precio con historial,
precio 0 rechazado (RN-01), baja de un vino con y sin historial (RN-14), ciclo completo de ingresos y
transferencias (incluida una transferencia rechazada por RN-11), tablero y vista móvil.
