// Transferencias a salas e ingresos al deposito comparten el mismo ciclo de vida
// (en_confeccion -> terminado -> procesado), asi que comparten pantallas.
import { api } from '../api.js';
import { fecha, numero } from '../util.js';
import { buscador, campo, confirmar, el, insignia, mostrarError, opciones, paginador, tabla, toast, vaciar } from '../ui.js';

const CONFIG = {
  transferencias: {
    base: '/transferencias', clave: 'nro_transferencia', titulo: 'Transferencias a salas', singular: 'Transferencia',
    ayuda: 'Pedido de vino del depósito central a una sala. Al procesarla se descuenta del depósito y se suma al stock de la sala.',
    columnas: [{ titulo: 'Sala', valor: (d) => d.sala }, { titulo: 'Fecha', valor: (d) => fecha(d.fecha_confeccion) }],
    datos: (d) => [['Sala', d.sala], ['Fecha de confección', fecha(d.fecha_confeccion)]],
    filtroExtra: async () => {
      const salas = await api.get('/salas');
      return { nombre: 'id_sala', etiqueta: 'Sala', control: opciones(el('select', {}), salas, (s) => s.id_sala, (s) => s.direccion, 'Todas') };
    },
    formularioAlta: async () => {
      const salas = await api.get('/salas');
      const sel = opciones(el('select', { required: true }), salas, (s) => s.id_sala, (s) => `${s.direccion} · ${s.localidad}`);
      return { controles: [campo('Sala destino', sel)], cuerpo: () => ({ id_sala: Number(sel.value) }) };
    },
  },
  ingresos: {
    base: '/ingresos', clave: 'cod_ingreso', titulo: 'Ingresos al depósito', singular: 'Ingreso',
    ayuda: 'Vino que llega de una bodega por un transportista. Al procesarlo se suma al stock del depósito central.',
    columnas: [{ titulo: 'Bodega', valor: (d) => d.bodega }, { titulo: 'Transportista', valor: (d) => d.transportista },
      { titulo: 'Fecha', valor: (d) => fecha(d.fecha) }],
    datos: (d) => [['Bodega', d.bodega], ['Transportista', d.transportista], ['Fecha', fecha(d.fecha)]],
    filtroExtra: async () => {
      const t = await api.get('/transportistas');
      return { nombre: 'cod_transportista', etiqueta: 'Transportista', control: opciones(el('select', {}), t, (x) => x.cod_transportista, (x) => x.razon_social, 'Todos') };
    },
    formularioAlta: async () => {
      const [t, b] = await Promise.all([api.get('/transportistas'), api.get('/bodegas')]);
      const st = opciones(el('select', { required: true }), t, (x) => x.cod_transportista, (x) => x.razon_social);
      const sb = opciones(el('select', { required: true }), b, (x) => x.cuit, (x) => x.razon_social);
      return { controles: [campo('Transportista', st), campo('Bodega de origen', sb)],
        cuerpo: () => ({ cod_transportista: Number(st.value), cuit_bodega: sb.value }) };
    },
  },
};

const ESTADOS_FILTRO = [['en_confeccion', 'En confección'], ['terminado', 'Terminado'], ['procesado', 'Procesado']];

export const vistaLista = (tipo) => async (cont, { query }) => {
  const cfg = CONFIG[tipo];
  const q = Object.fromEntries(query);
  const extra = await cfg.filtroExtra();
  extra.control.value = q[extra.nombre] || '';
  const estado = opciones(el('select', {}), ESTADOS_FILTRO, (x) => x[0], (x) => x[1], 'Todos');
  estado.value = q.estado || '';
  const resultado = el('div', { 'aria-live': 'polite' }, el('p', { class: 'cargando' }, 'Cargando…'));
  vaciar(cont).append(
    el('div', { class: 'encabezado' }, el('h1', {}, cfg.titulo), el('a', { class: 'btn btn-primario', href: `#/${tipo}/nueva` }, `＋ Nueva ${cfg.singular.toLowerCase()}`)),
    el('p', { class: 'ayuda' }, cfg.ayuda),
    el('form', { class: 'filtros', onsubmit: (ev) => {
      ev.preventDefault();
      const p = new URLSearchParams();
      if (estado.value) p.set('estado', estado.value);
      if (extra.control.value) p.set(extra.nombre, extra.control.value);
      location.hash = `#/${tipo}?${p}`;
    } }, campo('Estado', estado), campo(extra.etiqueta, extra.control),
    el('button', { class: 'btn btn-primario', type: 'submit' }, 'Filtrar'), el('a', { class: 'btn', href: `#/${tipo}` }, 'Limpiar')),
    resultado);
  try {
    const pag = await api.get(cfg.base, { ...q, page: q.page || 1, page_size: 15 });
    resultado.replaceChildren(tabla([
      { titulo: 'N.º', valor: (d) => d[cfg.clave] }, ...cfg.columnas,
      { titulo: 'Estado', valor: (d) => insignia(d.estado) },
      { titulo: 'Renglones', num: true, valor: (d) => numero(d.renglones) }, { titulo: 'Unidades', num: true, valor: (d) => numero(d.unidades) },
    ], pag.items.map((d) => ({ ...d, _alClick: () => { location.hash = `#/${tipo}/${d[cfg.clave]}`; } })), 'No hay documentos para esos filtros.'),
    paginador(pag, (p) => { const n = new URLSearchParams(q); n.set('page', p); location.hash = `#/${tipo}?${n}`; }));
  } catch (e) { mostrarError(resultado, e); }
};

/** Selector de renglones (vino + cantidad) reutilizado por el alta y por el detalle. */
function agregadorDeRenglones(alAgregar) {
  const cantidad = el('input', { type: 'number', min: '1', step: '1', value: '1', class: 'cant', 'aria-label': 'Cantidad' });
  let vino = null;
  const elegido = el('div', { class: 'seleccionado vacio' }, 'Elija un vino');
  const caja = el('div', { class: 'agregador' },
    buscador({ etiqueta: 'Vino', placeholder: 'Nombre del vino (2+ letras)…',
      buscar: async (t) => (await api.get('/vinos', { q: t, page_size: 8 })).items,
      describir: (v) => `${v.nombre} · ${v.anada} · depósito ${v.stock_deposito}`,
      alElegir: (v) => { vino = v; elegido.className = 'seleccionado'; elegido.textContent = v.nombre; } }),
    elegido, campo('Cantidad', cantidad),
    el('button', { type: 'button', class: 'btn', onclick: () => { if (vino) { alAgregar(vino, Number(cantidad.value)); } } }, 'Agregar renglón'));
  return caja;
}

export const vistaAlta = (tipo) => async (cont) => {
  const cfg = CONFIG[tipo];
  const alta = await cfg.formularioAlta();
  const renglones = [];
  const lista = el('div', {});
  const aviso = el('div', { 'aria-live': 'polite' });
  const pintar = () => lista.replaceChildren(renglones.length ? tabla([
    { titulo: 'Vino', valor: (r) => r.vino.nombre }, { titulo: 'Cantidad', num: true, valor: (r) => numero(r.cantidad) },
    { titulo: '', valor: (r) => el('button', { type: 'button', class: 'btn btn-chico', onclick: () => { renglones.splice(renglones.indexOf(r), 1); pintar(); } }, 'Quitar') },
  ], renglones) : el('p', { class: 'vacio' }, 'Todavía no hay renglones.'));
  pintar();
  vaciar(cont).append(
    el('p', {}, el('a', { href: `#/${tipo}` }, `‹ ${cfg.titulo}`)), el('h1', {}, `Nueva ${cfg.singular.toLowerCase()}`),
    el('p', { class: 'ayuda' }, 'Se crea EN CONFECCIÓN: todavía no mueve stock. Después hay que terminarla y procesarla.'),
    el('form', { class: 'formulario', onsubmit: async (ev) => {
      ev.preventDefault();
      try {
        const d = await api.post(cfg.base, { ...alta.cuerpo(), renglones: renglones.map((r) => ({ cod_vino: r.vino.cod_vino, cantidad: r.cantidad })) });
        toast(`${cfg.singular} N.º ${d[cfg.clave]} creada.`);
        location.hash = `#/${tipo}/${d[cfg.clave]}`;
      } catch (e) { mostrarError(aviso, e); }
    } },
    el('fieldset', {}, el('legend', {}, 'Datos'), ...alta.controles),
    el('fieldset', {}, el('legend', {}, 'Renglones'),
      agregadorDeRenglones((v, c) => { const ya = renglones.find((r) => r.vino.cod_vino === v.cod_vino); if (ya) ya.cantidad = c; else renglones.push({ vino: v, cantidad: c }); pintar(); }),
      lista),
    aviso, el('div', { class: 'acciones' }, el('a', { class: 'btn', href: `#/${tipo}` }, 'Cancelar'),
      el('button', { class: 'btn btn-primario', type: 'submit' }, 'Crear en confección'))));
};

export const vistaDetalle = (tipo) => async (cont, { params }) => {
  const cfg = CONFIG[tipo];
  const id = params[0];
  const zona = el('div', {}, el('p', { class: 'cargando' }, 'Cargando…'));
  vaciar(cont).append(zona);

  async function cargar() {
    const aviso = el('div', { 'aria-live': 'polite' });
    let d;
    try { d = await api.get(`${cfg.base}/${id}`); } catch (e) { mostrarError(zona, e); return; }
    const ejecutar = (ruta, ok, pedirConfirmacion) => async () => {
      if (pedirConfirmacion && !await confirmar(pedirConfirmacion.titulo, pedirConfirmacion.texto, pedirConfirmacion.boton)) return;
      try { await api.post(`${cfg.base}/${id}/${ruta}`); toast(ok); await cargar(); } catch (e) { mostrarError(aviso, e); }
    };
    const enConfeccion = d.estado === 'en_confeccion';
    zona.replaceChildren(
      el('p', {}, el('a', { href: `#/${tipo}` }, `‹ ${cfg.titulo}`)),
      el('div', { class: 'encabezado' }, el('h1', {}, `${cfg.singular} N.º ${d[cfg.clave]} `, insignia(d.estado)),
        el('div', { class: 'acciones' },
          enConfeccion ? el('button', { class: 'btn btn-primario', onclick: ejecutar('terminar', 'Documento terminado.') }, 'Terminar') : null,
          d.estado === 'terminado' ? el('button', { class: 'btn btn-primario', onclick: ejecutar('procesar', 'Procesado: el stock ya se movió.',
            { titulo: 'Procesar', texto: 'Esto mueve el stock y no se puede deshacer. ¿Continuar?', boton: 'Procesar' }) }, 'Procesar (mover stock)') : null)),
      aviso,
      el('section', { class: 'tarjeta' }, el('h2', {}, 'Datos'), el('dl', {}, ...cfg.datos(d).flatMap(([k, v]) => [el('dt', {}, k), el('dd', {}, v)]))),
      el('section', { class: 'tarjeta' }, el('h2', {}, 'Renglones'),
        tabla([{ titulo: 'Vino', valor: (r) => r.vino }, { titulo: 'Cantidad', num: true, valor: (r) => numero(r.cantidad) },
          enConfeccion ? { titulo: '', valor: (r) => el('button', { class: 'btn btn-chico', onclick: async () => {
            try { await api.borrar(`${cfg.base}/${id}/renglones/${r.cod_vino}`); await cargar(); } catch (e) { mostrarError(aviso, e); }
          } }, 'Quitar') } : null].filter(Boolean), d.detalle),
        enConfeccion ? agregadorDeRenglones(async (v, c) => {
          try { await api.post(`${cfg.base}/${id}/renglones`, { cod_vino: v.cod_vino, cantidad: c }); await cargar(); } catch (e) { mostrarError(aviso, e); }
        }) : el('p', { class: 'ayuda' }, 'Fuera de confección los renglones no se pueden modificar (RN-12).')));
  }
  await cargar();
};
