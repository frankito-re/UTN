// node --test "front/test/*.test.mjs"
import test from 'node:test';
import assert from 'node:assert/strict';
import { armarQuery, describirError, dinero, fecha, paginasVisibles, parsearHash, etiquetaEstado } from '../js/util.js';

test('armarQuery omite vacios y codifica todo (nada de texto crudo en la URL)', () => {
  assert.equal(armarQuery({ q: '', tipo: null, page: 2, ok: false }), '?page=2');
  assert.equal(armarQuery({}), '');
  assert.equal(armarQuery({ q: "' OR 1=1; --" }), "?q=%27+OR+1%3D1%3B+--");
  assert.equal(armarQuery({ q: 'a&b=c' }), '?q=a%26b%3Dc');
});

test('describirError traduce el cuerpo de la API', () => {
  const e = describirError(409, { error: { estado: 409, sqlstate: 'RN009', regla: 'RN-09', mensaje: 'Stock insuficiente del vino 7' } });
  assert.deepEqual([e.titulo, e.regla, e.mensaje], ['Conflicto', 'RN-09', 'Stock insuficiente del vino 7']);
  const v = describirError(400, { error: { mensaje: 'Peticion invalida.', detalle: [{ campo: 'query.page', problema: 'too small' }] } });
  assert.deepEqual(v.detalle, ['query.page: too small']);
  assert.equal(describirError(500, null).mensaje, 'No se pudo completar la operación.');
  assert.equal(describirError(500, null).titulo, 'Error del servidor');
});

test('formatos de presentacion', () => {
  assert.match(dinero(1234.5), /1\.234,50/);
  assert.equal(dinero(null), '—');
  assert.equal(fecha('2026-11-09'), '09/11/2026');
  assert.equal(fecha(null), '—');
  assert.equal(etiquetaEstado('en_confeccion'), 'En confección');
});

test('paginasVisibles', () => {
  assert.deepEqual(paginasVisibles(1, 3), [1, 2, 3]);
  assert.deepEqual(paginasVisibles(1, 20), [1, 2, 3, '…', 20]);
  assert.deepEqual(paginasVisibles(10, 20), [1, '…', 8, 9, 10, 11, 12, '…', 20]);
  assert.deepEqual(paginasVisibles(1, 0), []);
});

test('parsearHash', () => {
  assert.equal(parsearHash('').ruta, '/vinos');
  const h = parsearHash('#/vinos?q=malbec&page=2');
  assert.equal(h.ruta, '/vinos');
  assert.equal(h.query.get('q'), 'malbec');
});
