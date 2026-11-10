// Controles estaticos sobre el codigo del front:
//  1) nada de innerHTML/outerHTML/insertAdjacentHTML/eval/document.write (XSS);
//  2) las vistas no hacen cuentas con importes: los totales llegan calculados por la API.
import test from 'node:test';
import assert from 'node:assert/strict';
import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const raiz = fileURLToPath(new URL('../js/', import.meta.url));
const archivos = [];
(function recorrer(dir) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    if (e.isDirectory()) recorrer(join(dir, e.name)); else if (e.name.endsWith('.js')) archivos.push(join(dir, e.name));
  }
})(raiz);

test('hay codigo para revisar', () => assert.ok(archivos.length >= 8));

test('no se usa innerHTML ni equivalentes', () => {
  for (const a of archivos) {
    const src = readFileSync(a, 'utf8');
    for (const prohibido of ['innerHTML', 'outerHTML', 'insertAdjacentHTML', 'document.write', 'eval(', 'new Function']) {
      assert.ok(!src.includes(prohibido), `${a} usa ${prohibido}`);
    }
  }
});

test('el HTML no tiene scripts ni estilos en linea (compatible con la CSP)', () => {
  const html = readFileSync(fileURLToPath(new URL('../index.html', import.meta.url)), 'utf8');
  assert.ok(!/<script(?![^>]*\bsrc=)/i.test(html), 'script en linea');
  assert.ok(!/<style/i.test(html), 'style en linea');
  assert.ok(!/\sstyle=/i.test(html), 'atributo style');
  assert.ok(!/\son[a-z]+=/i.test(html), 'manejador de evento en linea');
});

test('las vistas de ventas y documentos no calculan importes', () => {
  for (const nombre of ['ventas.js', 'documentos.js']) {
    const src = readFileSync(join(raiz, 'vistas', nombre), 'utf8');
    assert.ok(!/\.reduce\(/.test(src), `${nombre} usa reduce (suma en el cliente)`);
    assert.ok(!/precio\w*\s*\*|\*\s*precio\w*|descuento\w*\s*\*|\*\s*descuento\w*/i.test(src), `${nombre} multiplica precios o descuentos`);
  }
});
