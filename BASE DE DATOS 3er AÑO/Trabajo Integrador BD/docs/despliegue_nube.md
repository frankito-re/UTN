# Despliegue en la nube y seguridad (Etapa 8)

> **Estado honesto.** Todo lo que se puede verificar sin una cuenta de nube **está verificado en una réplica local
> del despliegue de producción** (`docker-compose.prod.yml`): HTTPS, base con TLS, puertos restringidos, secretos fuera
> del repositorio, backup cifrado y restauración. Lo que falta es **publicarlo en un servidor real** (requiere una cuenta
> y, normalmente, un dominio): los pasos exactos están en la sección 3. La URL pública va en la sección 6 cuando exista.

## 1. Arquitectura de producción

```
Internet ──443/80──▶ [ proxy Caddy ]──▶ [ front nginx ]──/api──▶ [ API FastAPI ]──TLS──▶ [ PostgreSQL 16 ]
                      HTTPS + HSTS         CSP estricta            bodegas_api              hostssl + SCRAM
                      (Let's Encrypt)                              sin root, solo lectura   sin puerto publicado
```

* **Único puerto publicado: 80/443 del proxy.** Base, API y front viven en una red Docker `internal` **sin salida a internet**.
* **Base:** TLS obligatorio para conexiones de red (`hostssl`), `scram-sha-256`, TLS ≥ 1.2, solo los roles `bodegas_api` y
  `bodegas_ro` pueden conectarse por red; el propietario solo entra por el socket local (`docker compose exec`).
* **API:** conecta con `sslmode=verify-full` contra una CA propia, como `bodegas_api` (sin superusuario, sin DDL, sin escritura
  directa de stock/auditoría). Contenedor sin root, sistema de archivos de solo lectura, `cap_drop: ALL`, `no-new-privileges`.
* **Secretos:** solo en `.env.prod` (permisos 600, generado con `scripts/crear_env_prod.sh`) y `certs/` (ambos ignorados por git).

## 2. Controles verificados localmente

`scripts/verificar_despliegue.sh` ejecuta **29 controles** contra el stack de producción en marcha y falla si alguno no se cumple:

| Grupo | Controles |
| :-- | :-- |
| Exposición de red | base, API y front no publican puertos · el proxy publica solo 80/443 · nada escucha en el 5432 del host · la API no es alcanzable directo · las redes internas no tienen salida a internet |
| HTTPS | responde por HTTPS · HTTP redirige (308) · HSTS · CSP/nosniff/X-Frame-Options · sin cabecera `Server` · TLS 1.0/1.1 rechazados · la CSP no permite `unsafe-inline`/`unsafe-eval` |
| Base de datos | conexión sin TLS rechazada · con TLS y clave correcta aceptada · clave incorrecta rechazada · el propietario no entra por red · `bodegas_api` no es superusuario · **todas** las conexiones de la API van cifradas (TLS 1.3) · claves con SCRAM-SHA-256 |
| Contenedores y secretos | API sin root, sistema de archivos de solo lectura, sin capacidades, sin escalado de privilegios · ningún secreto aparece en archivos versionados · `.env`, `.env.prod`, `certs/`, `backups/` ignorados por git · la clave de la CA no está montada en ningún contenedor |

## 3. Publicarlo en un servidor (pasos exactos)

Camino recomendado: **una VPS con Docker** (Hetzner, DigitalOcean, AWS Lightsail, Oracle Cloud Free…). Es exactamente
el mismo stack que se probó localmente.

1. **Servidor:** Ubuntu 22.04/24.04, 2 GB de RAM como mínimo. Instalar Docker y el plugin compose.
2. **Dominio:** crear un registro DNS `A` (`app.midominio.com → IP del servidor`). Caddy obtiene el certificado de
   Let's Encrypt solo; necesita los puertos 80 y 443 abiertos.
3. **Firewall** (solo SSH, HTTP y HTTPS; la base nunca se abre):
   ```bash
   sudo ufw default deny incoming && sudo ufw allow OpenSSH && sudo ufw allow 80,443/tcp && sudo ufw enable
   ```
   Además: SSH solo con clave (`PasswordAuthentication no`), usuario no root, actualizaciones automáticas (`unattended-upgrades`).
4. **Código y secretos:**
   ```bash
   git clone <repo> bodegas && cd bodegas
   DOMINIO=app.midominio.com ACME_EMAIL=yo@correo.com scripts/crear_env_prod.sh   # claves aleatorias, chmod 600
   scripts/generar_certificados.sh                                               # CA + certificado TLS de la base
   docker compose --env-file .env.prod -f docker-compose.prod.yml up -d --build
   ```
5. **Datos:** la base se crea sola con las migraciones `001…008`. Para cargar los datos de prueba o los de otro entorno
   usar la **restauración** (sección 4) o el cargador (`db/seed/cargar_datos.py`, conectándose por el socket del contenedor).
6. **Verificar:** correr `scripts/verificar_despliegue.sh https://app.midominio.com` **en el servidor** (los controles
   miran los contenedores locales, así que no sirven desde otra máquina). Los de `HTTP_PORT`/`HTTPS_PORT` usan los valores de `.env.prod`.
7. **Guardar `.env.prod` y `certs/ca/ca.key` en un gestor de secretos** (1Password, Bitwarden, AWS Secrets Manager). Sin
   ellos no se puede reconstruir el servidor.

**Alternativa con base gestionada** (Neon, Supabase, RDS): subir la imagen de la API a Render/Railway/Fly.io y apuntar
`DB_HOST`/`DB_NAME`/`DB_USER`/`DB_PASSWORD` a la base gestionada con `DB_SSLMODE=require` (o `verify-full` con la CA del
proveedor). Hay que ejecutar `db/migrations/001…008` y crear los roles de `007_roles.sql` con sus claves
(`ALTER ROLE … PASSWORD …`). Los controles de la sección 2 sobre contenedores no aplican; los de HTTPS los da el proveedor.

## 4. Backup y restauración (probados)

| Script | Qué hace |
| :-- | :-- |
| `scripts/backup.sh` | `pg_dump -Fc` comprimido + suma SHA-256 + rotación (14 días por defecto). Con `BACKUP_CLAVE` se cifra con AES-256 y se borra el archivo en claro. |
| `scripts/restore.sh` | Verifica la suma (rechaza archivos alterados), descifra, crea los roles si faltan, restaura en una base **nueva** y reaplica lo que `pg_dump` no guarda (`CONNECT` y `random_page_cost`). Con `--forzar` reemplaza una base existente. |
| `scripts/probar_backup.sh` | **Simulacro:** backup cifrado → restauración en una base temporal → comparación contra el original → limpieza. |

`ENTORNO=prod` en cualquiera de ellos apunta al stack de producción; sin él, al de desarrollo.

**Qué compara el simulacro** (todo coincide, también en producción): filas de las 29 tablas, huellas MD5 del contenido de
`renglon_comprobante`, `cliente`, `vino` y `stock_sala`, cantidad de índices/triggers/funciones/vistas, privilegios de
`bodegas_api` y `bodegas_ro` (la API puede insertar vinos pero **no** stock; el rol de reportes no puede escribir), `CONNECT`
no concedido a PUBLIC, `fn_total_comprobante`, la vista materializada, y que `bodegas_api` entra por TCP a la base restaurada.

**Recuperación ante desastre probada:** se hizo un backup de la base de desarrollo y se restauró sobre el stack de
producción (`ENTORNO=prod scripts/restore.sh <archivo> bodegas_atuel --forzar` con la API detenida): la API por HTTPS
respondió con los 601 vinos restaurados.

**Programar los backups** (cron del servidor, diario a las 03:00, con copia fuera de la máquina):
```cron
0 3 * * *  cd /srv/bodegas && ENTORNO=prod BACKUP_CLAVE="$(cat /root/.clave_backup)" scripts/backup.sh >> /var/log/bodegas_backup.log 2>&1 \
           && rclone copy backups/ remoto:bodegas-backups/ --include "*.enc*"
```
Una copia en el mismo servidor no es un backup: hay que llevarla a otro lugar (S3/Backblaze/Drive vía `rclone`) y
**repetir el simulacro** (`scripts/probar_backup.sh`) periódicamente — un backup que nunca se restauró no se sabe si sirve.
La clave `BACKUP_CLAVE` se guarda aparte del archivo (gestor de secretos). Objetivos sugeridos: RPO 24 h, RTO < 30 min.

## 5. Checklist de seguridad (qué cubre cada ítem)

| Requisito del TP | Cómo se cumple | Evidencia |
| :-- | :-- | :-- |
| Roles con privilegios mínimos | `bodegas_owner` / `bodegas_api` (rw sin stock ni DDL) / `bodegas_ro`; REVOKE de PUBLIC | `db/tests/007_roles_test.sql`, `verificar_despliegue.sh` |
| Secretos fuera del repositorio | `.env`/`.env.prod`/`certs/` ignorados; claves por variables de entorno; script de claves aleatorias | control «ningún secreto en archivos versionados» |
| Conexión cifrada | TLS en la base (`hostssl`, `verify-full`) y HTTPS en el borde con HSTS | controles de HTTPS y de base |
| Puerto de la base restringido | no se publica; red interna sin internet; `pg_hba` solo `hostssl` para 2 roles | controles de exposición |
| Backup y restauración probados | `backup.sh` + `restore.sh` + `probar_backup.sh` (cifrado, integridad, comparación) | simulacro OK en desarrollo y producción |
| Inyección SQL | SQL parametrizado, lista blanca de `ORDER BY` | `api/tests/test_seguridad.py`, `api/demo_inyeccion.sh` |
| XSS | el front nunca inserta HTML; CSP sin `unsafe-inline` | `front/test/seguridad_estatica.test.mjs` |

**Riesgos conocidos y fuera de alcance** (para la defensa): no hay autenticación de usuarios finales (el TP no la pide: la API es
abierta detrás del proxy; en un uso real habría que agregar OIDC/JWT y límite de peticiones); `CORS` por defecto en desarrollo es
`*` (en producción se restringe al dominio); el backup lógico no permite recuperación a un instante exacto (PITR requiere WAL
archiving); los certificados de la base vencen a los 825 días y hay que rotarlos (`rm -r certs && scripts/generar_certificados.sh`).

## 6. URL pública

*Pendiente de publicar en un servidor real (ver sección 3).* Al hacerlo, completar:

* URL: `https://…`
* Fecha y proveedor: …
* Salida de `scripts/verificar_despliegue.sh` en el servidor: adjuntar.
