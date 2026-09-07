-- Devuelve  el producto más caro que existe en la tabla producto sin  hacer uso de MAX, ORDER BY ni LIMIT.
SELECT *
FROM producto
WHERE
    precio >= ALL (
        SELECT precio
        FROM producto
    )