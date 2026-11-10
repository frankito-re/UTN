import { api } from '../api.js';
import { dinero, numero } from '../util.js';
import { campo, el, mostrarError, opciones, tabla, toast, vaciar } from '../ui.js';

/** Barras horizontales. El ancho es solo presentacion (proporcion al maximo); los valores vienen de la API. */
function barras(filas, etiqueta, valor, formato) {
  if (!filas.length) return el('p', { class: 'vacio' }, 'Sin datos.');
  const max = Math.max(...filas.map(valor), 1);
  return el('ul', { class: 'barras' }, filas.map((f) => {
    const barra = el('span', { class: 'barra' });
    barra.style.setProperty('--ancho', `${(valor(f) / max) * 100}%`);
    return el('li', {}, el('span', { class: 'etiqueta' }, etiqueta(f)), el('span', { class: 'pista' }, barra), el('span', { class: 'valor' }, formato(f)));
  }));
}

export async function vistaTablero(cont) {
  const salas = await api.get('/salas');
  const selSala = opciones(el('select', {}), salas, (s) => s.id_sala, (s) => `${s.direccion} · ${s.localidad}`, 'Toda la red');
  const selSalaMes = opciones(el('select', {}), salas, (s) => s.id_sala, (s) => `${s.direccion} · ${s.localidad}`);
  const umbral = el('input', { type: 'number', min: '0', value: '50', class: 'cant' });
  const limite = opciones(el('select', {}), [5, 10, 15, 20], (x) => x, (x) => `Top ${x}`);
  limite.value = '10';
  const zTop = el('div', { 'aria-live': 'polite' }), zMes = el('div', { 'aria-live': 'polite' }), zStock = el('div', { 'aria-live': 'polite' });

  const cargarTop = async () => {
    try { const t = await api.get('/reportes/top-vinos', { limite: limite.value, id_sala: selSala.value });
      zTop.replaceChildren(barras(t, (v) => v.nombre, (v) => v.unidades, (v) => `${numero(v.unidades)} u. · ${dinero(v.importe)}`)); }
    catch (e) { mostrarError(zTop, e); }
  };
  const cargarMes = async () => {
    try { const p = await api.get('/reportes/ventas-mensuales', { id_sala: selSalaMes.value, page_size: 12 });
      const filas = [...p.items].reverse();
      zMes.replaceChildren(barras(filas, (m) => m.mes.slice(0, 7), (m) => m.total_vendido, (m) => `${dinero(m.total_vendido)} · ${numero(m.unidades)} u.`)); }
    catch (e) { mostrarError(zMes, e); }
  };
  const cargarStock = async () => {
    try { const p = await api.get('/reportes/stock-critico', { umbral: umbral.value || 0, page_size: 10 });
      zStock.replaceChildren(tabla([{ titulo: 'Vino', valor: (v) => v.nombre }, { titulo: 'Depósito', num: true, valor: (v) => numero(v.stock_deposito) },
        { titulo: 'Salas', num: true, valor: (v) => numero(v.stock_salas) }, { titulo: 'Total', num: true, valor: (v) => el('strong', {}, numero(v.stock_total)) }],
        p.items, 'Ningún vino por debajo del umbral.'), el('p', { class: 'ayuda' }, `${numero(p.total)} vinos por debajo del umbral.`)); }
    catch (e) { mostrarError(zStock, e); }
  };
  const refrescar = async () => {
    try { await api.post('/reportes/refrescar'); toast('Reportes actualizados.'); await cargarMes(); } catch (e) { toast(e.message, 'error'); }
  };
  selSala.addEventListener('change', cargarTop); limite.addEventListener('change', cargarTop);
  selSalaMes.addEventListener('change', cargarMes); umbral.addEventListener('change', cargarStock);

  vaciar(cont).append(
    el('div', { class: 'encabezado' }, el('h1', {}, 'Tablero de reportes'),
      el('button', { class: 'btn', onclick: refrescar }, '⟳ Actualizar reportes')),
    el('div', { class: 'grilla' },
      el('section', { class: 'tarjeta' }, el('h2', {}, 'Vinos más vendidos'), el('div', { class: 'filtros chicos' }, campo('Sala', selSala), campo('Cantidad', limite)), zTop),
      el('section', { class: 'tarjeta' }, el('h2', {}, 'Ventas mensuales por sala'), el('div', { class: 'filtros chicos' }, campo('Sala', selSalaMes)), zMes)),
    el('section', { class: 'tarjeta' }, el('h2', {}, 'Stock crítico'), el('div', { class: 'filtros chicos' }, campo('Umbral (stock total menor a)', umbral)), zStock));
  await Promise.all([cargarTop(), cargarMes(), cargarStock()]);
}
