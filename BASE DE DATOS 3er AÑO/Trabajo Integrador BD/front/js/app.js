import { api } from './api.js';
import { parsearHash } from './util.js';
import { el, mostrarError, vaciar } from './ui.js';
import { vistaCatalogo, vistaFicha, vistaFormVino } from './vistas/vinos.js';
import { vistaVentas, vistaVentaDetalle, vistaVentaNueva } from './vistas/ventas.js';
import { vistaAlta, vistaDetalle, vistaLista } from './vistas/documentos.js';
import { vistaTablero } from './vistas/tablero.js';

// El orden importa: las rutas literales ('nuevo', 'nueva') van antes que las que llevan id.
const RUTAS = [
  [/^\/vinos$/, vistaCatalogo], [/^\/vinos\/nuevo$/, vistaFormVino], [/^\/vinos\/(\d+)\/editar$/, vistaFormVino], [/^\/vinos\/(\d+)$/, vistaFicha],
  [/^\/ventas$/, vistaVentas], [/^\/ventas\/nueva$/, vistaVentaNueva], [/^\/ventas\/(\d+)$/, vistaVentaDetalle],
  [/^\/transferencias$/, vistaLista('transferencias')], [/^\/transferencias\/nueva$/, vistaAlta('transferencias')], [/^\/transferencias\/(\d+)$/, vistaDetalle('transferencias')],
  [/^\/ingresos$/, vistaLista('ingresos')], [/^\/ingresos\/nueva$/, vistaAlta('ingresos')], [/^\/ingresos\/(\d+)$/, vistaDetalle('ingresos')],
  [/^\/tablero$/, vistaTablero],
];
const SECCIONES = [['vinos', 'Catálogo'], ['ventas', 'Ventas'], ['transferencias', 'Transferencias'], ['ingresos', 'Ingresos'], ['tablero', 'Tablero']];

const main = document.getElementById('contenido');
const nav = document.getElementById('menu');
nav.append(...SECCIONES.map(([ruta, texto]) => el('a', { href: `#/${ruta}`, 'data-seccion': ruta }, texto)));

async function navegar() {
  const { ruta, query } = parsearHash(location.hash);
  const seccion = ruta.split('/')[1];
  nav.querySelectorAll('a').forEach((a) => a.classList.toggle('activo', a.dataset.seccion === seccion));
  for (const [patron, vista] of RUTAS) {
    const m = ruta.match(patron);
    if (m) {
      try { await vista(main, { params: m.slice(1), query }); }
      catch (e) { mostrarError(vaciar(main), e); }
      window.scrollTo({ top: 0 });
      return;
    }
  }
  vaciar(main).append(el('h1', {}, 'Página no encontrada'), el('p', {}, el('a', { href: '#/vinos' }, 'Volver al catálogo')));
}

async function estadoServicio() {
  const punto = document.getElementById('estado');
  try { await api.get('/health'); punto.className = 'estado ok'; punto.title = 'API y base de datos disponibles'; }
  catch { punto.className = 'estado mal'; punto.title = 'Sin conexión con la API'; }
}

window.addEventListener('hashchange', navegar);
estadoServicio(); setInterval(estadoServicio, 30000);
navegar();
