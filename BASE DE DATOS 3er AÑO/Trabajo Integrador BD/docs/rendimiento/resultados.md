# Resultados de rendimiento (generado)

Mediana de 7 ejecuciones con `EXPLAIN (ANALYZE, BUFFERS)`, cache caliente. «Bloques» = buffers compartidos tocados (hit + read) por la consulta. «Solo índices» = índices de 008 con la configuración por defecto del planificador; «Después» = índices + `random_page_cost = 1.1`.

| Consulta | Antes (ms) | Solo índices (ms) | Después (ms) | Mejora total | Bloques antes → después |
| :-- | --: | --: | --: | --: | --: |
| **Q1** Ventas por sala del último trimestre (S8) | 8.34 | 2.34 | 2.00 | 4.2× | 1,346 → 141 |
| **Q2** Últimas 20 compras de un cliente (ficha de cliente) | 6.18 | 0.03 | 0.02 | 294.5× | 1,334 → 23 |
| **Q3** Unidades vendidas de un vino por mes | 27.46 | 25.88 | 3.81 | 7.2× | 5,114 → 7,907 |
| **Q4** Top 10 vinos más vendidos de la red (S1) | 67.22 | 72.26 | 71.69 | 0.9× | 3,809 → 3,809 |
| **Q5** Clientes por tipo que compraron en una sala en la última semana (S3) | 5.60 | 0.06 | 0.04 | 147.4× | 1,365 → 37 |
| **Q6** Transferencias pendientes por sala (S5) | 0.26 | 0.06 | 0.05 | 5.3× | 30 → 2 |
| **Q7** Búsqueda de clientes por nombre (autocompletado) | 6.98 | 1.30 | 1.14 | 6.1× | 275 → 272 |
| **Q8** Salas con más pedidos de un vino en los últimos 15 días (S4) | 1.55 | 0.35 | 0.10 | 15.3× | 220 → 201 |
| **Q10** Ventas de toda la red en el último trimestre (tablero) | 6.72 | 1.53 | 1.47 | 4.6× | 1,334 → 72 |
| **Q9** Borrar un vino sin movimientos (verificación de FK, RN-14) | 22.51 | 0.17 | 0.28 | 79.3× | 5 → 5 |

## Costo de escritura

| | Sin índices | Con índices de 008 | Sobrecosto |
| :-- | --: | --: | --: |
| Registrar una venta (comprobante + 3 renglones, con triggers), ms | 0.749 | 0.901 | +20 % |
| Tamaño de la base | 85.5 MB | 112.6 MB | +27.1 MB |

## Tamaño de los índices de 008

| Índice | Tamaño |
| :-- | --: |
| `idx_renglon_comprobante_vino` | 12,952 kB |
| `idx_comprobante_sala_fecha` | 7,096 kB |
| `idx_comprobante_cliente_fecha` | 4,688 kB |
| `idx_renglon_transferencia_vino` | 1,576 kB |
| `idx_cliente_nombre_lower` | 624 kB |
| `idx_stock_sala_vino` | 224 kB |
| `idx_lote_uva_bodega` | 144 kB |
| `idx_auditoria_precio_vino` | 56 kB |
| `idx_renglon_ingreso_vino` | 56 kB |
| `brin_comprobante_fecha` | 24 kB |
| `idx_empleado_sala` | 16 kB |
| `idx_ingreso_bodega` | 16 kB |
| `idx_ingreso_transportista_fecha` | 16 kB |
| `idx_transferencia_pendientes` | 16 kB |
| `idx_vino_bodega` | 16 kB |
| **Total** | **27,520 kB** |

## Planes

### Q1 · Ventas por sala del último trimestre (S8)

**Antes:** Seq Scan en comprobante; Seq Scan en sala_venta

**Después:** Index Scan (sala_venta_pkey) en sala_venta; Index Only Scan (idx_comprobante_sala_fecha) en comprobante

<details><summary>Plan antes</summary>

```
Sort  (cost=4022.80..4022.90 rows=40 width=82) (actual time=7.246..8.220 rows=40 loops=1)
  Sort Key: (sum(c.total)) DESC
  Sort Method: quicksort  Memory: 27kB
  Buffers: shared hit=1346
  ->  Finalize GroupAggregate  (cost=4015.94..4021.74 rows=40 width=82) (actual time=7.187..8.203 rows=40 loops=1)
        Group Key: s.id_sala
        Buffers: shared hit=1346
        ->  Gather Merge  (cost=4015.94..4020.54 rows=40 width=50) (actual time=7.182..8.164 rows=80 loops=1)
              Workers Planned: 1
              Workers Launched: 1
              Buffers: shared hit=1346
              ->  Sort  (cost=3015.93..3016.03 rows=40 width=50) (actual time=6.113..6.116 rows=40 loops=2)
                    Sort Key: s.id_sala
                    Sort Method: quicksort  Memory: 29kB
                    Buffers: shared hit=1346
                    Worker 0:  Sort Method: quicksort  Memory: 29kB
                    ->  Partial HashAggregate  (cost=3014.36..3014.86 rows=40 width=50) (actual time=6.091..6.101 rows=40 loops=2)
                          Group Key: s.id_sala
                          Batches: 1  Memory Usage: 48kB
                          Buffers: shared hit=1339
                          Worker 0:  Batches: 1  Memory Usage: 48kB
                          ->  Hash Join  (cost=1.90..2994.49 rows=3974 width=24) (actual time=4.645..5.612 rows=3330 loops=2)
                                Hash Cond: (c.id_sala = s.id_sala)
                                Buffers: shared hit=1339
                                ->  Parallel Seq Scan on comprobante c  (cost=0.00..2981.06 rows=3974 width=10) (actual time=4.617..4.995 rows=3330 loops=2)
                                      Filter: (fecha >= (CURRENT_DATE - 90))
                                      Rows Removed by Filter: 76670
                                      Buffers: shared hit=1334
                                ->  Hash  (cost=1.40..1.40 rows=40 width=18) (actual time=0.015..0.015 rows=40 loops=2)
                                      Buckets: 1024  Batches: 1  Memory Usage: 11kB
                                      Buffers: shared hit=2
                                      ->  Seq Scan on sala_venta s  (cost=0.00..1.40 rows=40 width=18) (actual time=0.005..0.008 rows=40 loops=2)
                                            Buffers: shared hit=2
Planning:
  Buffers: shared hit=8
Planning Time: 0.146 ms
Execution Time: 8.248 ms
```
</details>

<details><summary>Plan después</summary>

```
Sort  (cost=312.07..312.17 rows=40 width=82) (actual time=1.893..1.895 rows=40 loops=1)
  Sort Key: (sum(c.total)) DESC
  Sort Method: quicksort  Memory: 27kB
  Buffers: shared hit=141
  ->  GroupAggregate  (cost=0.56..311.00 rows=40 width=82) (actual time=0.095..1.882 rows=40 loops=1)
        Group Key: s.id_sala
        Buffers: shared hit=141
        ->  Nested Loop  (cost=0.56..275.04 rows=7013 width=24) (actual time=0.009..1.304 rows=6659 loops=1)
              Buffers: shared hit=141
              ->  Index Scan using sala_venta_pkey on sala_venta s  (cost=0.14..4.04 rows=40 width=18) (actual time=0.002..0.006 rows=40 loops=1)
                    Buffers: shared hit=2
              ->  Index Only Scan using idx_comprobante_sala_fecha on comprobante c  (cost=0.42..5.02 rows=175 width=10) (actual time=0.003..0.015 rows=166 loops=40)
                    Index Cond: ((id_sala = s.id_sala) AND (fecha >= (CURRENT_DATE - 90)))
                    Heap Fetches: 0
                    Buffers: shared hit=139
Planning:
  Buffers: shared hit=9
Planning Time: 0.084 ms
Execution Time: 1.910 ms
```
</details>

### Q2 · Últimas 20 compras de un cliente (ficha de cliente)

**Antes:** Seq Scan en comprobante

**Después:** Index Scan (idx_comprobante_cliente_fecha) en comprobante

<details><summary>Plan antes</summary>

```
Limit  (cost=3334.27..3334.30 rows=14 width=14) (actual time=6.352..6.356 rows=20 loops=1)
  Buffers: shared hit=1334
  ->  Sort  (cost=3334.27..3334.30 rows=14 width=14) (actual time=6.352..6.353 rows=20 loops=1)
        Sort Key: fecha DESC
        Sort Method: quicksort  Memory: 26kB
        Buffers: shared hit=1334
        ->  Seq Scan on comprobante  (cost=0.00..3334.00 rows=14 width=14) (actual time=0.255..6.342 rows=26 loops=1)
              Filter: (id_cliente = 13519)
              Rows Removed by Filter: 159974
              Buffers: shared hit=1334
Planning Time: 0.040 ms
Execution Time: 6.366 ms
```
</details>

<details><summary>Plan después</summary>

```
Limit  (cost=0.42..23.23 rows=20 width=14) (actual time=0.004..0.012 rows=20 loops=1)
  Buffers: shared hit=23
  ->  Index Scan using idx_comprobante_cliente_fecha on comprobante  (cost=0.42..55.16 rows=48 width=14) (actual time=0.004..0.010 rows=20 loops=1)
        Index Cond: (id_cliente = 13519)
        Buffers: shared hit=23
Planning Time: 0.023 ms
Execution Time: 0.017 ms
```
</details>

### Q3 · Unidades vendidas de un vino por mes

**Antes:** Seq Scan en comprobante; Seq Scan en renglon_comprobante

**Después:** Bitmap Heap Scan en renglon_comprobante; Bitmap Index Scan (idx_renglon_comprobante_vino) en ?; Index Scan (comprobante_pkey) en comprobante

<details><summary>Plan antes</summary>

```
Finalize GroupAggregate  (cost=9955.46..10119.95 rows=1623 width=12) (actual time=25.801..27.462 rows=83 loops=1)
  Group Key: ((date_trunc('month'::text, (c.fecha)::timestamp with time zone))::date)
  Buffers: shared hit=5114
  ->  Gather Merge  (cost=9955.46..10086.77 rows=955 width=12) (actual time=25.796..27.436 rows=166 loops=1)
        Workers Planned: 1
        Workers Launched: 1
        Buffers: shared hit=5114
        ->  Partial GroupAggregate  (cost=8955.45..8979.33 rows=955 width=12) (actual time=24.547..24.672 rows=83 loops=2)
              Group Key: ((date_trunc('month'::text, (c.fecha)::timestamp with time zone))::date)
              Buffers: shared hit=5114
              ->  Sort  (cost=8955.45..8957.84 rows=955 width=8) (actual time=24.541..24.590 rows=819 loops=2)
                    Sort Key: ((date_trunc('month'::text, (c.fecha)::timestamp with time zone))::date)
                    Sort Method: quicksort  Memory: 53kB
                    Buffers: shared hit=5114
                    Worker 0:  Sort Method: quicksort  Memory: 48kB
                    ->  Parallel Hash Join  (cost=6378.77..8908.18 rows=955 width=8) (actual time=10.829..24.431 rows=819 loops=2)
                          Hash Cond: (c.nro_comprobante = r.nro_comprobante)
                          Buffers: shared hit=5077
                          ->  Parallel Seq Scan on comprobante c  (cost=0.00..2275.18 rows=94118 width=8) (actual time=0.004..6.587 rows=80000 loops=2)
                                Buffers: shared hit=1334
                          ->  Parallel Hash  (cost=6370.32..6370.32 rows=676 width=8) (actual time=10.738..10.738 rows=819 loops=2)
                                Buckets: 2048  Batches: 1  Memory Usage: 112kB
                                Buffers: shared hit=3729
                                ->  Parallel Seq Scan on renglon_comprobante r  (cost=0.00..6370.32 rows=676 width=8) (actual time=0.030..10.534 rows=819 loops=2)
                                      Filter: (cod_vino = 50)
                                      Rows Removed by Filter: 252748
                                      Buffers: shared hit=3729
Planning:
  Buffers: shared hit=16
Planning Time: 0.154 ms
Execution Time: 27.490 ms
```
</details>

<details><summary>Plan después</summary>

```
GroupAggregate  (cost=3968.28..4010.96 rows=1707 width=12) (actual time=3.656..3.875 rows=83 loops=1)
  Group Key: ((date_trunc('month'::text, (c.fecha)::timestamp with time zone))::date)
  Buffers: shared hit=7907
  ->  Sort  (cost=3968.28..3972.55 rows=1707 width=8) (actual time=3.652..3.740 rows=1638 loops=1)
        Sort Key: ((date_trunc('month'::text, (c.fecha)::timestamp with time zone))::date)
        Sort Method: quicksort  Memory: 100kB
        Buffers: shared hit=7907
        ->  Nested Loop  (cost=20.67..3876.64 rows=1707 width=8) (actual time=0.251..3.469 rows=1638 loops=1)
              Buffers: shared hit=7907
              ->  Bitmap Heap Scan on renglon_comprobante r  (cost=20.25..1485.72 rows=1707 width=8) (actual time=0.248..1.042 rows=1638 loops=1)
                    Recheck Cond: (cod_vino = 50)
                    Heap Blocks: exact=1348
                    Buffers: shared hit=1355
                    ->  Bitmap Index Scan on idx_renglon_comprobante_vino  (cost=0.00..19.82 rows=1707 width=0) (actual time=0.122..0.123 rows=1638 loops=1)
                          Index Cond: (cod_vino = 50)
                          Buffers: shared hit=7
              ->  Index Scan using comprobante_pkey on comprobante c  (cost=0.42..1.39 rows=1 width=8) (actual time=0.001..0.001 rows=1 loops=1638)
                    Index Cond: (nro_comprobante = r.nro_comprobante)
                    Buffers: shared hit=6552
Planning:
  Buffers: shared hit=16
Planning Time: 0.093 ms
Execution Time: 3.895 ms
```
</details>

### Q4 · Top 10 vinos más vendidos de la red (S1)

**Antes:** Seq Scan en renglon_comprobante; Seq Scan en vino

**Después:** Seq Scan en renglon_comprobante; Seq Scan en vino

<details><summary>Plan antes</summary>

```
Limit  (cost=8689.37..8689.39 rows=10 width=37) (actual time=66.445..67.489 rows=10 loops=1)
  Buffers: shared hit=3809
  ->  Sort  (cost=8689.37..8690.87 rows=600 width=37) (actual time=66.444..67.486 rows=10 loops=1)
        Sort Key: (sum(r.cantidad)) DESC
        Sort Method: top-N heapsort  Memory: 26kB
        Buffers: shared hit=3809
        ->  Finalize GroupAggregate  (cost=8524.39..8676.40 rows=600 width=37) (actual time=65.840..67.400 rows=600 loops=1)
              Group Key: v.cod_vino
              Buffers: shared hit=3809
              ->  Gather Merge  (cost=8524.39..8664.40 rows=1200 width=37) (actual time=65.835..67.173 rows=1800 loops=1)
                    Workers Planned: 2
                    Workers Launched: 2
                    Buffers: shared hit=3809
                    ->  Sort  (cost=7524.37..7525.87 rows=600 width=37) (actual time=64.021..64.066 rows=600 loops=3)
                          Sort Key: v.cod_vino
                          Sort Method: quicksort  Memory: 63kB
                          Buffers: shared hit=3809
                          Worker 0:  Sort Method: quicksort  Memory: 63kB
                          Worker 1:  Sort Method: quicksort  Memory: 63kB
                          ->  Partial HashAggregate  (cost=7490.68..7496.68 rows=600 width=37) (actual time=63.782..63.848 rows=600 loops=3)
                                Group Key: v.cod_vino
                                Batches: 1  Memory Usage: 105kB
                                Buffers: shared hit=3795
                                Worker 0:  Batches: 1  Memory Usage: 105kB
                                Worker 1:  Batches: 1  Memory Usage: 105kB
                                ->  Hash Join  (cost=33.50..6434.15 rows=211306 width=33) (actual time=0.171..43.213 rows=169045 loops=3)
                                      Hash Cond: (r.cod_vino = v.cod_vino)
                                      Buffers: shared hit=3795
                                      ->  Parallel Seq Scan on renglon_comprobante r  (cost=0.00..5842.06 rows=211306 width=8) (actual time=0.006..14.992 rows=169045 loops=3)
                                            Buffers: shared hit=3729
                                      ->  Hash  (cost=26.00..26.00 rows=600 width=29) (actual time=0.148..0.148 rows=600 loops=3)
                                            Buckets: 1024  Batches: 1  Memory Usage: 45kB
                                            Buffers: shared hit=60
                                            ->  Seq Scan on vino v  (cost=0.00..26.00 rows=600 width=29) (actual time=0.011..0.076 rows=600 loops=3)
                                                  Buffers: shared hit=60
Planning:
  Buffers: shared hit=12
Planning Time: 0.146 ms
Execution Time: 67.518 ms
```
</details>

<details><summary>Plan después</summary>

```
Limit  (cost=8689.37..8689.39 rows=10 width=37) (actual time=65.768..66.802 rows=10 loops=1)
  Buffers: shared hit=3809
  ->  Sort  (cost=8689.37..8690.87 rows=600 width=37) (actual time=65.767..66.800 rows=10 loops=1)
        Sort Key: (sum(r.cantidad)) DESC
        Sort Method: top-N heapsort  Memory: 26kB
        Buffers: shared hit=3809
        ->  Finalize GroupAggregate  (cost=8524.39..8676.40 rows=600 width=37) (actual time=65.208..66.718 rows=600 loops=1)
              Group Key: v.cod_vino
              Buffers: shared hit=3809
              ->  Gather Merge  (cost=8524.39..8664.40 rows=1200 width=37) (actual time=65.204..66.495 rows=1800 loops=1)
                    Workers Planned: 2
                    Workers Launched: 2
                    Buffers: shared hit=3809
                    ->  Sort  (cost=7524.37..7525.87 rows=600 width=37) (actual time=63.551..63.584 rows=600 loops=3)
                          Sort Key: v.cod_vino
                          Sort Method: quicksort  Memory: 63kB
                          Buffers: shared hit=3809
                          Worker 0:  Sort Method: quicksort  Memory: 63kB
                          Worker 1:  Sort Method: quicksort  Memory: 63kB
                          ->  Partial HashAggregate  (cost=7490.68..7496.68 rows=600 width=37) (actual time=63.374..63.434 rows=600 loops=3)
                                Group Key: v.cod_vino
                                Batches: 1  Memory Usage: 105kB
                                Buffers: shared hit=3795
                                Worker 0:  Batches: 1  Memory Usage: 105kB
                                Worker 1:  Batches: 1  Memory Usage: 105kB
                                ->  Hash Join  (cost=33.50..6434.15 rows=211306 width=33) (actual time=0.161..43.041 rows=169045 loops=3)
                                      Hash Cond: (r.cod_vino = v.cod_vino)
                                      Buffers: shared hit=3795
                                      ->  Parallel Seq Scan on renglon_comprobante r  (cost=0.00..5842.06 rows=211306 width=8) (actual time=0.007..14.769 rows=169045 loops=3)
                                            Buffers: shared hit=3729
                                      ->  Hash  (cost=26.00..26.00 rows=600 width=29) (actual time=0.141..0.142 rows=600 loops=3)
                                            Buckets: 1024  Batches: 1  Memory Usage: 45kB
                                            Buffers: shared hit=60
                                            ->  Seq Scan on vino v  (cost=0.00..26.00 rows=600 width=29) (actual time=0.009..0.068 rows=600 loops=3)
                                                  Buffers: shared hit=60
Planning:
  Buffers: shared hit=20
Planning Time: 0.176 ms
Execution Time: 66.836 ms
```
</details>

### Q5 · Clientes por tipo que compraron en una sala en la última semana (S3)

**Antes:** Seq Scan en comprobante; Index Only Scan (cliente_id_cliente_tipo_cliente_key) en cliente

**Después:** Index Scan (idx_comprobante_sala_fecha) en comprobante; Index Only Scan (cliente_id_cliente_tipo_cliente_key) en cliente

<details><summary>Plan antes</summary>

```
GroupAggregate  (cost=4247.90..4248.02 rows=3 width=14) (actual time=4.548..5.517 rows=1 loops=1)
  Group Key: cl.tipo_cliente
  Buffers: shared hit=1365
  ->  Sort  (cost=4247.90..4247.93 rows=12 width=10) (actual time=4.543..5.512 rows=14 loops=1)
        Sort Key: cl.tipo_cliente, c.id_cliente
        Sort Method: quicksort  Memory: 25kB
        Buffers: shared hit=1365
        ->  Gather  (cost=1000.29..4247.69 rows=12 width=10) (actual time=4.467..5.503 rows=14 loops=1)
              Workers Planned: 1
              Workers Launched: 1
              Buffers: shared hit=1365
              ->  Nested Loop  (cost=0.29..3246.49 rows=7 width=10) (actual time=3.545..3.570 rows=7 loops=2)
                    Buffers: shared hit=1365
                    ->  Parallel Seq Scan on comprobante c  (cost=0.00..3216.35 rows=7 width=4) (actual time=3.533..3.542 rows=7 loops=2)
                          Filter: ((id_sala = 7) AND (fecha >= (CURRENT_DATE - 7)))
                          Rows Removed by Filter: 79993
                          Buffers: shared hit=1334
                    ->  Index Only Scan using cliente_id_cliente_tipo_cliente_key on cliente cl  (cost=0.29..4.30 rows=1 width=10) (actual time=0.003..0.003 rows=1 loops=14)
                          Index Cond: (id_cliente = c.id_cliente)
                          Heap Fetches: 0
                          Buffers: shared hit=31
Planning:
  Buffers: shared hit=6
Planning Time: 0.118 ms
Execution Time: 5.534 ms
```
</details>

<details><summary>Plan después</summary>

```
GroupAggregate  (cost=52.79..52.98 rows=3 width=14) (actual time=0.028..0.028 rows=1 loops=1)
  Group Key: cl.tipo_cliente
  Buffers: shared hit=37
  ->  Sort  (cost=52.79..52.85 rows=21 width=10) (actual time=0.025..0.026 rows=14 loops=1)
        Sort Key: cl.tipo_cliente, c.id_cliente
        Sort Method: quicksort  Memory: 25kB
        Buffers: shared hit=37
        ->  Nested Loop  (cost=0.71..52.33 rows=21 width=10) (actual time=0.005..0.020 rows=14 loops=1)
              Buffers: shared hit=37
              ->  Index Scan using idx_comprobante_sala_fecha on comprobante c  (cost=0.42..25.03 rows=21 width=4) (actual time=0.003..0.005 rows=14 loops=1)
                    Index Cond: ((id_sala = 7) AND (fecha >= (CURRENT_DATE - 7)))
                    Buffers: shared hit=8
              ->  Index Only Scan using cliente_id_cliente_tipo_cliente_key on cliente cl  (cost=0.29..1.30 rows=1 width=10) (actual time=0.001..0.001 rows=1 loops=14)
                    Index Cond: (id_cliente = c.id_cliente)
                    Heap Fetches: 0
                    Buffers: shared hit=29
Planning:
  Buffers: shared hit=15
Planning Time: 0.077 ms
Execution Time: 0.036 ms
```
</details>

### Q6 · Transferencias pendientes por sala (S5)

**Antes:** Seq Scan en transferencia

**Después:** Index Only Scan (idx_transferencia_pendientes) en transferencia

<details><summary>Plan antes</summary>

```
Sort  (cost=100.85..100.94 rows=39 width=12) (actual time=0.257..0.259 rows=39 loops=1)
  Sort Key: (count(*))
  Sort Method: quicksort  Memory: 26kB
  Buffers: shared hit=30
  ->  HashAggregate  (cost=99.43..99.82 rows=39 width=12) (actual time=0.249..0.253 rows=39 loops=1)
        Group Key: id_sala
        Batches: 1  Memory Usage: 24kB
        Buffers: shared hit=30
        ->  Seq Scan on transferencia  (cost=0.00..98.62 rows=160 width=4) (actual time=0.196..0.228 rows=160 loops=1)
              Filter: (estado <> 'procesado'::estado_documento)
              Rows Removed by Filter: 5330
              Buffers: shared hit=30
Planning Time: 0.015 ms
Execution Time: 0.267 ms
```
</details>

<details><summary>Plan después</summary>

```
Sort  (cost=6.97..7.06 rows=39 width=12) (actual time=0.034..0.036 rows=39 loops=1)
  Sort Key: (count(*))
  Sort Method: quicksort  Memory: 26kB
  Buffers: shared hit=2
  ->  GroupAggregate  (cost=0.14..5.93 rows=39 width=12) (actual time=0.004..0.030 rows=39 loops=1)
        Group Key: id_sala
        Buffers: shared hit=2
        ->  Index Only Scan using idx_transferencia_pendientes on transferencia  (cost=0.14..4.74 rows=160 width=4) (actual time=0.003..0.014 rows=160 loops=1)
              Heap Fetches: 0
              Buffers: shared hit=2
Planning Time: 0.020 ms
Execution Time: 0.043 ms
```
</details>

### Q7 · Búsqueda de clientes por nombre (autocompletado)

**Antes:** Seq Scan en cliente

**Después:** Bitmap Heap Scan en cliente; Bitmap Index Scan (idx_cliente_nombre_lower) en ?

<details><summary>Plan antes</summary>

```
Limit  (cost=578.32..578.45 rows=50 width=21) (actual time=7.065..7.072 rows=50 loops=1)
  Buffers: shared hit=275
  ->  Sort  (cost=578.32..578.57 rows=100 width=21) (actual time=7.065..7.068 rows=50 loops=1)
        Sort Key: nombre_razon_social
        Sort Method: top-N heapsort  Memory: 30kB
        Buffers: shared hit=275
        ->  Seq Scan on cliente  (cost=0.00..575.00 rows=100 width=21) (actual time=0.009..6.503 rows=989 loops=1)
              Filter: (lower((nombre_razon_social)::text) ~~ 'gonz%'::text)
              Rows Removed by Filter: 19011
              Buffers: shared hit=275
Planning Time: 0.018 ms
Execution Time: 7.078 ms
```
</details>

<details><summary>Plan después</summary>

```
Limit  (cost=329.99..330.11 rows=50 width=21) (actual time=1.225..1.232 rows=50 loops=1)
  Buffers: shared hit=272
  ->  Sort  (cost=329.99..332.15 rows=865 width=21) (actual time=1.224..1.227 rows=50 loops=1)
        Sort Key: nombre_razon_social
        Sort Method: top-N heapsort  Memory: 30kB
        Buffers: shared hit=272
        ->  Bitmap Heap Scan on cliente  (cost=13.44..301.25 rows=865 width=21) (actual time=0.067..0.657 rows=989 loops=1)
              Filter: (lower((nombre_razon_social)::text) ~~ 'gonz%'::text)
              Heap Blocks: exact=267
              Buffers: shared hit=272
              ->  Bitmap Index Scan on idx_cliente_nombre_lower  (cost=0.00..13.23 rows=854 width=0) (actual time=0.046..0.047 rows=989 loops=1)
                    Index Cond: ((lower((nombre_razon_social)::text) ~>=~ 'gonz'::text) AND (lower((nombre_razon_social)::text) ~<~ 'gon{'::text))
                    Buffers: shared hit=5
Planning Time: 0.047 ms
Execution Time: 1.240 ms
```
</details>

### Q8 · Salas con más pedidos de un vino en los últimos 15 días (S4)

**Antes:** Seq Scan en renglon_transferencia; Seq Scan en transferencia

**Después:** Index Only Scan (idx_renglon_transferencia_vino) en renglon_transferencia; Index Scan (transferencia_pkey) en transferencia

<details><summary>Plan antes</summary>

```
Limit  (cost=758.73..758.74 rows=3 width=12) (actual time=1.560..1.561 rows=3 loops=1)
  Buffers: shared hit=220
  ->  Sort  (cost=758.73..758.74 rows=3 width=12) (actual time=1.560..1.561 rows=3 loops=1)
        Sort Key: (sum(rt.cantidad)) DESC
        Sort Method: quicksort  Memory: 25kB
        Buffers: shared hit=220
        ->  GroupAggregate  (cost=758.66..758.71 rows=3 width=12) (actual time=1.556..1.558 rows=3 loops=1)
              Group Key: t.id_sala
              Buffers: shared hit=220
              ->  Sort  (cost=758.66..758.67 rows=3 width=8) (actual time=1.554..1.555 rows=3 loops=1)
                    Sort Key: t.id_sala
                    Sort Method: quicksort  Memory: 25kB
                    Buffers: shared hit=220
                    ->  Hash Join  (cost=129.36..758.63 rows=3 width=8) (actual time=1.512..1.553 rows=3 loops=1)
                          Hash Cond: (rt.nro_transferencia = t.nro_transferencia)
                          Buffers: shared hit=220
                          ->  Seq Scan on renglon_transferencia rt  (cost=0.00..629.09 rows=70 width=8) (actual time=0.005..1.216 rows=66 loops=1)
                                Filter: (cod_vino = 50)
                                Rows Removed by Filter: 35061
                                Buffers: shared hit=190
                          ->  Hash  (cost=126.08..126.08 rows=263 width=8) (actual time=0.330..0.330 rows=262 loops=1)
                                Buckets: 1024  Batches: 1  Memory Usage: 19kB
                                Buffers: shared hit=30
                                ->  Seq Scan on transferencia t  (cost=0.00..126.08 rows=263 width=8) (actual time=0.277..0.301 rows=262 loops=1)
                                      Filter: (fecha_confeccion >= (CURRENT_DATE - 15))
                                      Rows Removed by Filter: 5228
                                      Buffers: shared hit=30
Planning:
  Buffers: shared hit=12
Planning Time: 0.107 ms
Execution Time: 1.572 ms
```
</details>

<details><summary>Plan después</summary>

```
Limit  (cost=74.97..74.98 rows=3 width=12) (actual time=0.081..0.082 rows=3 loops=1)
  Buffers: shared hit=201
  ->  Sort  (cost=74.97..74.98 rows=3 width=12) (actual time=0.081..0.081 rows=3 loops=1)
        Sort Key: (sum(rt.cantidad)) DESC
        Sort Method: quicksort  Memory: 25kB
        Buffers: shared hit=201
        ->  GroupAggregate  (cost=74.89..74.95 rows=3 width=12) (actual time=0.078..0.079 rows=3 loops=1)
              Group Key: t.id_sala
              Buffers: shared hit=201
              ->  Sort  (cost=74.89..74.90 rows=3 width=8) (actual time=0.077..0.077 rows=3 loops=1)
                    Sort Key: t.id_sala
                    Sort Method: quicksort  Memory: 25kB
                    Buffers: shared hit=201
                    ->  Nested Loop  (cost=0.57..74.87 rows=3 width=8) (actual time=0.073..0.076 rows=3 loops=1)
                          Buffers: shared hit=201
                          ->  Index Only Scan using idx_renglon_transferencia_vino on renglon_transferencia rt  (cost=0.29..2.56 rows=67 width=8) (actual time=0.003..0.008 rows=66 loops=1)
                                Index Cond: (cod_vino = 50)
                                Heap Fetches: 0
                                Buffers: shared hit=3
                          ->  Index Scan using transferencia_pkey on transferencia t  (cost=0.28..1.08 rows=1 width=8) (actual time=0.001..0.001 rows=0 loops=66)
                                Index Cond: (nro_transferencia = rt.nro_transferencia)
                                Filter: (fecha_confeccion >= (CURRENT_DATE - 15))
                                Rows Removed by Filter: 1
                                Buffers: shared hit=198
Planning:
  Buffers: shared hit=12
Planning Time: 0.091 ms
Execution Time: 0.091 ms
```
</details>

### Q10 · Ventas de toda la red en el último trimestre (tablero)

**Antes:** Seq Scan en comprobante

**Después:** Bitmap Heap Scan en comprobante; Bitmap Index Scan (brin_comprobante_fecha) en ?

<details><summary>Plan antes</summary>

```
Finalize Aggregate  (cost=4001.05..4001.06 rows=1 width=40) (actual time=6.016..7.112 rows=1 loops=1)
  Buffers: shared hit=1334
  ->  Gather  (cost=4000.93..4001.04 rows=1 width=40) (actual time=5.950..7.106 rows=2 loops=1)
        Workers Planned: 1
        Workers Launched: 1
        Buffers: shared hit=1334
        ->  Partial Aggregate  (cost=3000.93..3000.94 rows=1 width=40) (actual time=4.826..4.826 rows=1 loops=2)
              Buffers: shared hit=1334
              ->  Parallel Seq Scan on comprobante  (cost=0.00..2981.06 rows=3974 width=6) (actual time=4.183..4.512 rows=3330 loops=2)
                    Filter: (fecha >= (CURRENT_DATE - 90))
                    Rows Removed by Filter: 76670
                    Buffers: shared hit=1334
Planning Time: 0.060 ms
Execution Time: 7.131 ms
```
</details>

<details><summary>Plan después</summary>

```
Aggregate  (cost=1507.47..1507.48 rows=1 width=40) (actual time=1.406..1.407 rows=1 loops=1)
  Buffers: shared hit=72
  ->  Bitmap Heap Scan on comprobante  (cost=5.07..1472.41 rows=7013 width=6) (actual time=0.139..0.803 rows=6659 loops=1)
        Recheck Cond: (fecha >= (CURRENT_DATE - 90))
        Rows Removed by Index Recheck: 1661
        Heap Blocks: lossy=70
        Buffers: shared hit=72
        ->  Bitmap Index Scan on brin_comprobante_fecha  (cost=0.00..3.32 rows=7619 width=0) (actual time=0.010..0.010 rows=700 loops=1)
              Index Cond: (fecha >= (CURRENT_DATE - 90))
              Buffers: shared hit=2
Planning:
  Buffers: shared hit=1
Planning Time: 0.027 ms
Execution Time: 1.414 ms
```
</details>

### Q9 · Borrar un vino sin movimientos (verificación de FK, RN-14)

**Antes:** Index Scan (vino_pkey) en vino

**Después:** Index Scan (vino_pkey) en vino

<details><summary>Plan antes</summary>

```
Delete on vino  (cost=0.28..8.29 rows=0 width=0) (actual time=0.009..0.009 rows=0 loops=1)
  Buffers: shared hit=5
  ->  Index Scan using vino_pkey on vino  (cost=0.28..8.29 rows=1 width=6) (actual time=0.003..0.004 rows=1 loops=1)
        Index Cond: (cod_vino = 609)
        Buffers: shared hit=3
Planning Time: 0.015 ms
Trigger for constraint composicion_cod_vino_fkey: time=0.014 calls=1
Trigger for constraint vino_maridaje_cod_vino_fkey: time=0.009 calls=1
Trigger for constraint renglon_comprobante_cod_vino_fkey: time=20.840 calls=1
Trigger for constraint renglon_ingreso_cod_vino_fkey: time=0.093 calls=1
Trigger for constraint renglon_transferencia_cod_vino_fkey: time=1.402 calls=1
Trigger for constraint stock_sala_cod_vino_fkey: time=0.814 calls=1
Trigger for constraint stock_deposito_cod_vino_fkey: time=0.016 calls=1
Trigger for constraint auditoria_precio_cod_vino_fkey: time=0.054 calls=1
Execution Time: 23.260 ms
```
</details>

<details><summary>Plan después</summary>

```
Delete on vino  (cost=0.28..2.49 rows=0 width=0) (actual time=0.018..0.018 rows=0 loops=1)
  Buffers: shared hit=5
  ->  Index Scan using vino_pkey on vino  (cost=0.28..2.49 rows=1 width=6) (actual time=0.010..0.010 rows=1 loops=1)
        Index Cond: (cod_vino = 609)
        Buffers: shared hit=3
Planning Time: 0.041 ms
Trigger for constraint composicion_cod_vino_fkey: time=0.014 calls=1
Trigger for constraint vino_maridaje_cod_vino_fkey: time=0.007 calls=1
Trigger for constraint renglon_comprobante_cod_vino_fkey: time=0.040 calls=1
Trigger for constraint renglon_ingreso_cod_vino_fkey: time=0.011 calls=1
Trigger for constraint renglon_transferencia_cod_vino_fkey: time=0.012 calls=1
Trigger for constraint stock_sala_cod_vino_fkey: time=0.009 calls=1
Trigger for constraint stock_deposito_cod_vino_fkey: time=0.009 calls=1
Trigger for constraint auditoria_precio_cod_vino_fkey: time=0.006 calls=1
Execution Time: 0.138 ms
```
</details>
