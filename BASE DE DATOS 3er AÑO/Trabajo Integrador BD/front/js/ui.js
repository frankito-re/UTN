// Utilidades de interfaz. REGLA: los datos se insertan SIEMPRE como texto (nodos de texto),
// nunca como HTML, para que ningun dato de la base pueda inyectar etiquetas o scripts (XSS).
import { ESTADOS, paginasVisibles } from './util.js';

/** Constructor de elementos: el('div', {class:'x', onclick: fn}, 'texto', otroNodo) */
export function el(etiqueta, atributos = {}, ...hijos) {
  const nodo = document.createElement(etiqueta);
  for (const [k, v] of Object.entries(atributos || {})) {
    if (v === null || v === undefined || v === false) continue;
    if (k.startsWith('on') && typeof v === 'function') nodo.addEventListener(k.slice(2), v);
    else if (k === 'class') nodo.className = v;
    else if (k === 'value') nodo.value = v;
    else if (v === true) nodo.setAttribute(k, '');
    else nodo.setAttribute(k, String(v));
  }
  agregar(nodo, hijos);
  return nodo;
}

export function agregar(padre, hijos) {
  for (const h of hijos.flat(Infinity)) {
    if (h === null || h === undefined || h === false) continue;
    padre.append(h instanceof Node ? h : document.createTextNode(String(h)));
  }
  return padre;
}

export const vaciar = (nodo) => { nodo.replaceChildren(); return nodo; };

export function toast(mensaje, tipo = 'ok', ms = 4500) {
  let zona = document.getElementById('toasts');
  if (!zona) { zona = el('div', { id: 'toasts', 'aria-live': 'polite' }); document.body.append(zona); }
  const t = el('div', { class: `toast toast-${tipo}`, role: 'status' }, mensaje);
  zona.append(t);
  setTimeout(() => t.remove(), ms);
}

/** Cartel de error de negocio, con la regla y el detalle que mando la API. */
export function cartelError(info) {
  return el('div', { class: 'cartel cartel-error', role: 'alert' },
    el('strong', {}, info.titulo, info.regla ? ` · ${info.regla}` : ''),
    el('p', {}, info.mensaje),
    info.detalle.length ? el('ul', {}, info.detalle.map((d) => el('li', {}, d))) : null);
}

export function mostrarError(contenedor, e) {
  const info = e && e.info ? e.info : { titulo: 'Error', mensaje: String(e && e.message ? e.message : e), regla: null, detalle: [] };
  contenedor.replaceChildren(cartelError(info));
  contenedor.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

export function confirmar(titulo, mensaje, textoAceptar = 'Aceptar') {
  return new Promise((resolver) => {
    const cerrar = (r) => { fondo.remove(); resolver(r); };
    const fondo = el('div', { class: 'modal-fondo', onclick: (ev) => { if (ev.target === fondo) cerrar(false); } },
      el('div', { class: 'modal', role: 'dialog', 'aria-modal': 'true' },
        el('h3', {}, titulo), el('p', {}, mensaje),
        el('div', { class: 'acciones' },
          el('button', { class: 'btn', onclick: () => cerrar(false) }, 'Cancelar'),
          el('button', { class: 'btn btn-peligro', onclick: () => cerrar(true) }, textoAceptar))));
    document.body.append(fondo);
  });
}

export function insignia(estado) {
  return el('span', { class: `insignia insignia-${estado}` }, ESTADOS[estado] || estado);
}

export function paginador(pagina, alCambiar) {
  const { page, pages, total, page_size: tam } = pagina;
  const desde = total ? (page - 1) * tam + 1 : 0;
  const hasta = Math.min(page * tam, total);
  return el('nav', { class: 'paginador', 'aria-label': 'Paginación' },
    el('span', { class: 'cuenta' }, total ? `${desde}–${hasta} de ${total}` : 'Sin resultados'),
    el('div', { class: 'botones' },
      el('button', { class: 'btn btn-chico', disabled: page <= 1, onclick: () => alCambiar(page - 1) }, '‹ Anterior'),
      paginasVisibles(page, pages).map((p) => p === '…' ? el('span', { class: 'hueco' }, '…') :
        el('button', { class: `btn btn-chico${p === page ? ' activo' : ''}`, onclick: () => alCambiar(p), 'aria-current': p === page ? 'page' : null }, String(p))),
      el('button', { class: 'btn btn-chico', disabled: page >= pages, onclick: () => alCambiar(page + 1) }, 'Siguiente ›')));
}

export function tabla(columnas, filas, vacio = 'Sin datos.') {
  if (!filas.length) return el('p', { class: 'vacio' }, vacio);
  return el('div', { class: 'tabla-scroll' },
    el('table', {},
      el('thead', {}, el('tr', {}, columnas.map((c) => el('th', { class: c.num ? 'num' : null }, c.titulo)))),
      el('tbody', {}, filas.map((f) => {
        const tr = el('tr', f._alClick ? { class: 'clicable', tabindex: 0, onclick: f._alClick,
          onkeydown: (ev) => { if (ev.key === 'Enter') f._alClick(); } } : {},
          columnas.map((c) => el('td', { class: c.num ? 'num' : null }, c.valor(f))));
        return tr;
      }))));
}

export function campo(etiqueta, control, ayuda) {
  return el('label', { class: 'campo' }, el('span', {}, etiqueta), control, ayuda ? el('small', {}, ayuda) : null);
}

export function opciones(select, items, valor, texto, vacio) {
  select.replaceChildren();
  if (vacio) select.append(el('option', { value: '' }, vacio));
  for (const it of items) select.append(el('option', { value: valor(it) }, texto(it)));
  return select;
}

/** Caja de busqueda con sugerencias: consulta a la API mientras se escribe. */
export function buscador({ etiqueta, placeholder, buscar, describir, alElegir }) {
  const entrada = el('input', { type: 'search', placeholder, autocomplete: 'off' });
  const lista = el('ul', { class: 'sugerencias', hidden: true });
  let temporizador;
  entrada.addEventListener('input', () => {
    clearTimeout(temporizador);
    const q = entrada.value.trim();
    if (q.length < 2) { lista.hidden = true; return; }
    temporizador = setTimeout(async () => {
      try {
        const items = await buscar(q);
        lista.replaceChildren(...items.map((it) => el('li', { tabindex: 0, onclick: () => elegir(it),
          onkeydown: (ev) => { if (ev.key === 'Enter') elegir(it); } }, describir(it))));
        if (!items.length) lista.replaceChildren(el('li', { class: 'sin-resultados' }, 'Sin coincidencias'));
        lista.hidden = false;
      } catch (e) { lista.hidden = true; toast(e.message, 'error'); }
    }, 250);
  });
  function elegir(it) { lista.hidden = true; entrada.value = ''; alElegir(it); }
  return el('div', { class: 'buscador' }, el('label', { class: 'campo' }, el('span', {}, etiqueta), entrada), lista);
}
