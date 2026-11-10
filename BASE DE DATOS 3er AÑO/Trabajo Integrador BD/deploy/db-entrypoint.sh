#!/bin/bash
# Arranca PostgreSQL con TLS y con el pg_hba.conf de produccion.
# Copia certificado, clave y pg_hba a un directorio propio del contenedor para fijar
# dueño y permisos (la clave debe ser 0600 y de postgres), sin tocar los archivos montados.
set -euo pipefail
DEST=/var/lib/postgresql/tls
mkdir -p "$DEST"
cp /certs-src/server.crt /certs-src/server.key "$DEST/"
cp /deploy/pg_hba.conf "$DEST/pg_hba.conf"
chown -R postgres:postgres "$DEST"
chmod 600 "$DEST/server.key"
chmod 644 "$DEST/server.crt" "$DEST/pg_hba.conf"
exec docker-entrypoint.sh postgres \
  -c ssl=on \
  -c ssl_cert_file="$DEST/server.crt" \
  -c ssl_key_file="$DEST/server.key" \
  -c ssl_min_protocol_version=TLSv1.2 \
  -c hba_file="$DEST/pg_hba.conf" \
  -c password_encryption=scram-sha-256 \
  -c log_connections=on
