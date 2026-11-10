#!/usr/bin/env bash
# CA propia + certificado TLS para PostgreSQL (SAN: db y localhost). La API verifica contra la CA (verify-full).
# Salida: certs/ca/ca.crt (publico, se monta en la API), certs/ca/ca.key (secreto, no sale de aca),
#         certs/db/server.crt y server.key. Todo en certs/, ignorado por git.
set -euo pipefail
cd "$(dirname "$0")/.."
DIAS="${DIAS:-825}"
[ -e certs/db/server.crt ] && { echo "certs/ ya existe: no se regenera (borre la carpeta para rotar)."; exit 0; }
mkdir -p certs/ca certs/db
umask 077
openssl genrsa -out certs/ca/ca.key 4096 2>/dev/null
openssl req -x509 -new -key certs/ca/ca.key -sha256 -days 3650 -subj "/O=Bodegas del Atuel/CN=Bodegas del Atuel CA" -out certs/ca/ca.crt
openssl genrsa -out certs/db/server.key 2048 2>/dev/null
openssl req -new -key certs/db/server.key -subj "/O=Bodegas del Atuel/CN=db" -out certs/db/server.csr
cat > certs/db/ext.cnf <<EXT
subjectAltName = DNS:db, DNS:localhost
basicConstraints = CA:FALSE
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
EXT
openssl x509 -req -in certs/db/server.csr -CA certs/ca/ca.crt -CAkey certs/ca/ca.key -CAcreateserial \
  -sha256 -days "$DIAS" -extfile certs/db/ext.cnf -out certs/db/server.crt 2>/dev/null
rm -f certs/db/server.csr certs/db/ext.cnf certs/ca/ca.srl
chmod 644 certs/ca/ca.crt certs/db/server.crt; chmod 600 certs/ca/ca.key certs/db/server.key
echo "Certificados generados en certs/ (vencen en $DIAS dias; renovar antes)."
openssl x509 -in certs/db/server.crt -noout -subject -enddate -ext subjectAltName 2>/dev/null || true
