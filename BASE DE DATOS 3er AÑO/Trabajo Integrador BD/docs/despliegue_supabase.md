# Publicación con Supabase (base) + Render (aplicación)

**Por qué dos servicios:** Supabase aloja la **base de datos PostgreSQL**, pero no corre contenedores propios, así que la API y el front
(un solo contenedor, [`Dockerfile.cloud`](../Dockerfile.cloud)) van en un servicio de hosting. Esta guía usa **Render** (plan gratuito, sin tarjeta).
Cualquier plataforma de contenedores sirve (Railway, Koyeb, Fly.io): solo hay que definir la variable `DATABASE_URL`.

```
Navegador ──HTTPS──▶ Render (contenedor: front en / + API en /api) ──TLS──▶ Supabase PostgreSQL (rol bodegas_api, vía Session pooler)
```

## Qué ya está hecho y probado

| Pieza | Estado |
| :-- | :-- |
| Imagen única API + front (`Dockerfile.cloud`), cabeceras de seguridad, `DATABASE_URL` | construida y probada: front, `/api/health`, datos, Swagger, ventas y procedimientos de stock |
| Migraciones tolerantes a un Postgres gestionado (sin superusuario ni dueño de la base) | probadas contra un Postgres **emulando a Supabase**: usuario no superusuario, base de otro dueño, roles `anon`/`authenticated`/`service_role` y privilegios por defecto como los de Supabase |
| `deploy/supabase/endurecer.sql`: cierra la API REST automática de Supabase (PostgREST) sobre nuestras tablas | verificado: `anon`, `authenticated` y `service_role` no pueden leer nada |
| `scripts/supabase_instalar.py`: migraciones + roles + endurecimiento + carga + verificación | probado en la emulación (incluye que la API **no** puede escribir stock directo) |
| Backup/restauración remotos (`backup_remoto.sh`, `probar_backup_remoto.sh`) | probados con la base de desarrollo haciendo de servidor remoto: 40 valores idénticos entre origen y copia |
| `scripts/verificar_publicado.sh <url>`: 14 controles de solo lectura sobre la URL pública | probado contra la imagen local |
| **Lo que no se pudo probar sin tu cuenta:** el proyecto real de Supabase y el servicio real de Render | pasos 1 a 5 de abajo |

## Pasos (los 1, 4 y 5 los hacés vos: requieren tu cuenta y tus claves)

### 1. Crear el proyecto en Supabase
1. https://supabase.com → **New project**. Nombre `bodegas-del-atuel`, región lo más cercana posible (ej. *South America (São Paulo)*).
2. **Database password:** usá «Generate a password», **guardala** (gestor de contraseñas). No hay forma de verla después (solo cambiarla).
3. Esperar a que termine de aprovisionar. En el plan gratuito la base tiene 500 MB; el proyecto usa ~105 MB.
4. Botón **Connect** (arriba) → **Session pooler** (puerto **5432**) → copiar la cadena `postgresql://postgres.<ref>:[YOUR-PASSWORD]@aws-…pooler.supabase.com:5432/postgres`
   y reemplazar `[YOUR-PASSWORD]` por la clave del paso 2. *(Se usa el Session pooler y no la conexión directa porque esta última es solo IPv6 en el plan gratuito;
   y no el «Transaction pooler» (6543) porque el driver usa sentencias preparadas y transacciones largas.)*
5. Crear el archivo `.env.supabase` en la raíz del proyecto (está en `.gitignore`) con una sola línea:
   ```
   SUPABASE_DB_URL=postgresql://postgres.<ref>:<CLAVE>@aws-…pooler.supabase.com:5432/postgres
   ```
   *(Opcional y recomendado: Project Settings → Data API → desactivar «Enable Data API». El script de instalación ya deja sin acceso a esa API, pero así queda cerrada también por configuración.)*

### 2. Instalar la base (un comando)
```bash
.venv/bin/python scripts/supabase_instalar.py --cargar        # --escala 0.2 para una carga más chica
```
Aplica las migraciones `001…008`, crea los roles `bodegas_api` y `bodegas_ro` con claves aleatorias (se guardan en `.env.supabase`), cierra la API REST
automática, carga los datos y **verifica**: 29 tablas, `anon`/`authenticated`/`service_role` sin acceso, el rol de la API entra por el pooler, no puede escribir stock directo
y lee el catálogo. Al final escribe `.env.supabase.render` con la línea `DATABASE_URL=…` lista para pegar en Render. Ninguna clave se imprime.

### 3. Repositorio para Render
**No hace falta un repositorio nuevo.** Render despliega desde el repositorio que ya tenés (`frankito-re/UTN`) indicando la carpeta del proyecto como *Root Directory*.
Solo hay que **subir la rama** `bd-tpi-bodegas-del-atuel` a GitHub (`git push -u origin bd-tpi-bodegas-del-atuel`) y conectar ese repositorio en Render (autorizar la app de Render en GitHub).
*(El `render.yaml` solo lo lee Render si está en la raíz del repositorio; como acá el proyecto está en una subcarpeta, se usa la creación manual del servicio del paso 4.)*

Riesgo a tener en cuenta: la ruta de la carpeta tiene espacios y una «Ñ». Si Render no la acepta, el plan B es un repositorio propio del TP (ver «Plan B» al final).

### 4. Crear el servicio en Render
1. https://render.com → **New → Web Service** → conectar el repositorio `UTN` y elegir la rama `bd-tpi-bodegas-del-atuel`.
2. *Language* **Docker**, *Root Directory* `BASE DE DATOS 3er AÑO/Trabajo Integrador BD`, *Dockerfile Path* `./Dockerfile.cloud`, *Instance type* **Free**, *Health Check Path* `/api/health`.
3. **Environment → `DATABASE_URL`**: pegar el valor de `.env.supabase.render` (es un secreto: Render lo guarda cifrado y no aparece en el repositorio).
4. **Create**. Cuando termine el build, la URL queda tipo `https://bodegas-del-atuel.onrender.com`.

### 5. Verificar lo publicado y registrar la URL
```bash
scripts/verificar_publicado.sh https://bodegas-del-atuel.onrender.com
```
Controla HTTPS y redirección, HSTS, CSP estricta, TLS ≥ 1.2, que el front cargue, que la API llegue a Supabase, Swagger, y que 3 ataques de inyección SQL no hagan nada.
Después: poner la URL en el [README](../README.md) y en la sección 6 de [despliegue_nube.md](despliegue_nube.md), y guardar la salida del script como evidencia.

## Seguridad: qué cambia en Supabase

* **API REST automática (PostgREST).** Supabase expone `public` a `anon`/`authenticated` con una clave pública. `endurecer.sql` les revoca todo, incluidos los
  privilegios por defecto de tablas futuras, y desactiva RLS (no hace falta: solo los roles de la aplicación tienen privilegios). Si no se hiciera, **cualquiera con la clave `anon` podría leer las tablas**.
* **Cifrado.** La conexión usa `sslmode=require` (cifrada) hacia Supabase. Para verificar además el certificado (`verify-full`) hay que bajar el certificado raíz de Supabase
  (Project Settings → Database → SSL) y montarlo en la imagen: mejora opcional.
* **Mínimo privilegio.** La API usa `bodegas_api.<ref>` (el pooler exige el sufijo `.<ref>`): sin superusuario, sin DDL, sin escritura directa de stock/auditoría. El propietario
  (`postgres`) solo se usa para instalar y para los backups.
* **Secretos.** `.env.supabase` y `.env.supabase.render` están en `.gitignore`; en Render la clave vive solo en el panel de variables de entorno.
* **Puertos.** No hay nada que restringir en el contenedor (solo expone el puerto HTTP de la plataforma, detrás de su TLS). En Supabase se pueden limitar las IP de origen en
  *Network Restrictions*, pero Render gratuito no tiene IP fija: se deja abierto a internet protegido por TLS y por la clave.

## Backup y restauración con Supabase

El plan gratuito **no incluye backups descargables**, así que se hacen con los scripts del proyecto (usan el cliente `pg_dump` de una imagen Docker, no hace falta instalar nada):
```bash
scripts/backup_remoto.sh                       # backups/remoto_<fecha>.sql.gz  (+ .sha256; con BACKUP_CLAVE=… se cifra con AES-256)
scripts/probar_backup_remoto.sh                # SIMULACRO: backup remoto -> restauración en una base local temporal -> comparación -> limpieza
ENTORNO=dev scripts/restore.sh backups/remoto_….sql.gz[.enc] mi_base_nueva    # restaurar a mano
```
El simulacro compara contra Supabase las 29 tablas, huellas de contenido, estructura y privilegios, y rechaza archivos alterados. **Hay que correrlo una vez contra el proyecto real**
y guardar la salida: es la evidencia de «backup y restauración probados» para este despliegue. Para programarlo, ver el cron de [despliegue_nube.md](despliegue_nube.md#4-backup-y-restauración-probados).

## Limitaciones del plan gratuito (para saberlas antes de la defensa)

* **Render se duerme** tras ~15 min sin tráfico y tarda alrededor de un minuto en despertar: **abrir la URL unos minutos antes** de presentar.
* **Supabase pausa** los proyectos gratuitos tras ~1 semana sin actividad (se reactiva desde el panel con «Restore project»): entrar antes de la fecha.
* 500 MB de base; el Session pooler limita las conexiones simultáneas (la imagen usa un pool de 5).

## Problemas frecuentes

| Síntoma | Causa probable |
| :-- | :-- |
| `Tenant or user not found` | región o referencia del proyecto mal copiada: usar exactamente la cadena de *Connect → Session pooler* |
| `password authentication failed for user "bodegas_api…"` | el rol se conecta como `bodegas_api.<ref>` (con el sufijo); revisar `.env.supabase.render` |
| `could not translate host name` / `Network is unreachable` | se usó la conexión *Direct* (IPv6): usar el Session pooler |
| `/api/health` da 503 recién desplegado | el contenedor despierta o `DATABASE_URL` está vacía en Render |
| El instalador dice «el rol … todavía puede acceder a las tablas» | el endurecimiento no pudo quitar privilegios: reportar el mensaje; **no publicar** hasta resolverlo |

## Plan B: repositorio propio del TP (solo si Render no acepta la ruta)

`git subtree` falla con la «Ñ» del nombre de la carpeta, así que se usa `filter-branch` sobre una copia temporal (el repositorio original no se modifica):
```bash
TOP="$(git rev-parse --show-toplevel)"
git clone --no-local --branch bd-tpi-bodegas-del-atuel --single-branch "$TOP" /tmp/bodegas && cd /tmp/bodegas
FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f --subdirectory-filter "BASE DE DATOS 3er AÑO/Trabajo Integrador BD" -- --all
git branch -M main && git remote remove origin
gh repo create <usuario>/bodegas-del-atuel --private --source . --push
```
