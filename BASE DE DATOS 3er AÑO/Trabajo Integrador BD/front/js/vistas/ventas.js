import { api } from '../api.js';
import { dinero, fecha, numero } from '../util.js';
import { buscador, campo, el, mostrarError, opciones, paginador, tabla, toast, vaciar } from '../ui.js';

export async function vistaVentas(cont, { query }) {
  const q = Object.fromEntries(query);
  const salas = await api.get('/salas');
  const sala = opciones(el('select', {}), salas, (s) => s.id_sala, (s) => `${s.direccion} · ${s.localidad}`, 'Todas las salas');
  sala.value = q.id_sala || '';
  const desde = el('input', { type: 'date', value: q.desde || '' });
  const hasta = el('input', { type: 'date', value: q.hasta || '' });
  const resultado = el('div', { 'aria-live': 'polite' }, el('p', { class: 'cargando' }, 'Cargando…'));
  vaciar(cont).append(
    el('div', { class: 'encabezado' }, el('h1', {}, 'Ventas'), el('a', { class: 'btn btn-primario', href: '#/ventas/nueva' }, '＋ Nueva venta')),
    el('form', { class: 'filtros', onsubmit: (ev) => {
      ev.preventDefault();
      const p = new URLSearchParams();
      if (sala.value) p.set('id_sala', sala.value);
      if (desde.value) p.set('desde', desde.value);
      if (hasta.value) p.set('hasta', hasta.value);
      location.hash = `#/ventas?${p}`;
    } }, campo('Sala', sala), campo('Desde', desde), campo('Hasta', hasta),
    el('button', { class: 'btn btn-primario', type: 'submit' }, 'Filtrar'), el('a', { class: 'btn', href: '#/ventas' }, 'Limpiar')),
    resultado);
  try {
    const pag = await api.get('/comprobantes', { ...q, page: q.page || 1, page_size: 15 });
    resultado.replaceChildren(tabla([
      { titulo: 'N.º', valor: (c) => c.nro_comprobante }, { titulo: 'Fecha', valor: (c) => fecha(c.fecha) },
      { titulo: 'Cliente', valor: (c) => c.cliente }, { titulo: 'Tipo', valor: (c) => c.tipo_cliente },
      { titulo: 'Sala', valor: (c) => `${c.sala} · ${c.localidad_sala}` },
      { titulo: 'Unidades', num: true, valor: (c) => numero(c.unidades) },
      { titulo: 'Descuento', num: true, valor: (c) => dinero(c.descuento) }, { titulo: 'Total', num: true, valor: (c) => el('strong', {}, dinero(c.total)) },
    ], pag.items.map((c) => ({ ...c, _alClick: () => { location.hash = `#/ventas/${c.nro_comprobante}`; } })), 'No hay ventas para esos filtros.'),
    paginador(pag, (p) => { const n = new URLSearchParams(q); n.set('page', p); location.hash = `#/ventas?${n}`; }));
  } catch (e) { mostrarError(resultado, e); }
}

export async function vistaVentaDetalle(cont, { params }) {
  const zona = el('div', {}, el('p', { class: 'cargando' }, 'Cargando…'));
  vaciar(cont).append(zona);
  try {
    const c = await api.get(`/comprobantes/${params[0]}`);
    zona.replaceChildren(
      el('p', {}, el('a', { href: '#/ventas' }, '‹ Ventas')),
      el('h1', {}, `Comprobante N.º ${c.nro_comprobante}`),
      el('div', { class: 'grilla' },
        el('section', { class: 'tarjeta' }, el('h2', {}, 'Datos'),
          el('dl', {}, ...[['Fecha', fecha(c.fecha)], ['Cliente', `${c.cliente} (${c.tipo_cliente})`], ['Sala', `${c.sala} · ${c.localidad_sala}`]]
            .flatMap(([k, v]) => [el('dt', {}, k), el('dd', {}, v)]))),
        el('section', { class: 'tarjeta totales' }, el('h2', {}, 'Importes calculados por la base'),
          el('dl', {}, ...[['Subtotal', dinero(c.subtotal)], ['Descuento', dinero(c.descuento)], ['Total', dinero(c.total)]]
            .flatMap(([k, v]) => [el('dt', {}, k), el('dd', {}, v)])))),
      el('section', { class: 'tarjeta' }, el('h2', {}, 'Renglones'),
        tabla([{ titulo: 'Vino', valor: (r) => r.vino }, { titulo: 'Cantidad', num: true, valor: (r) => numero(r.cantidad) },
          { titulo: 'Precio unit.', num: true, valor: (r) => dinero(r.precio_unitario) },
          { titulo: 'Desc. %', num: true, valor: (r) => r.descuento_pct }, { titulo: 'Subtotal', num: true, valor: (r) => dinero(r.subtotal) }], c.detalle)));
  } catch (e) { mostrarError(zona, e); }
}

/** Nueva venta. El formulario SOLO envia cliente, sala, vinos y cantidades: precios, descuento,
 *  totales y stock los calcula la base de datos y se muestran en el comprobante resultante. */
export async function vistaVentaNueva(cont) {
  const salas = await api.get('/salas');
  let cliente = null;
  const renglones = [];                     // {vino, cantidad}
  const sala = opciones(el('select', { required: true }), salas, (s) => s.id_sala, (s) => `${s.direccion} · ${s.localidad}`);
  const aviso = el('div', { 'aria-live': 'polite' });
  const cajaCliente = el('div', { class: 'seleccionado vacio' }, 'Ningún cliente elegido');
  const listaReng = el('div', {});

  const pintarCliente = () => {
    cajaCliente.className = cliente ? 'seleccionado' : 'seleccionado vacio';
    cajaCliente.replaceChildren(cliente
      ? el('span', {}, el('strong', {}, cliente.nombre_razon_social), ` · ${cliente.tipo_cliente} · doc. ${cliente.nro_doc}`)
      : 'Ningún cliente elegido');
  };
  const pintarRenglones = () => {
    listaReng.replaceChildren(renglones.length ? tabla([
      { titulo: 'Vino', valor: (r) => r.vino.nombre },
      { titulo: 'Stock total', num: true, valor: (r) => numero(r.vino.stock_total) },
      { titulo: 'Cantidad', num: true, valor: (r) => {
        const inp = el('input', { type: 'number', min: '1', step: '1', value: r.cantidad, 'aria-label': `Cantidad de ${r.vino.nombre}`, class: 'cant' });
        inp.addEventListener('input', () => { r.cantidad = inp.value; });
        return inp;
      } },
      { titulo: '', valor: (r) => el('button', { type: 'button', class: 'btn btn-chico', onclick: () => { renglones.splice(renglones.indexOf(r), 1); pintarRenglones(); } }, 'Quitar') },
    ], renglones) : el('p', { class: 'vacio' }, 'Todavía no hay vinos en la venta.'));
  };
  pintarCliente(); pintarRenglones();

  const enviar = async (ev) => {
    ev.preventDefault();
    if (!cliente) { mostrarError(aviso, { info: { titulo: 'Falta el cliente', mensaje: 'Elija un cliente para la venta.', regla: null, detalle: [] } }); return; }
    try {
      const c = await api.post('/comprobantes', {
        id_cliente: cliente.id_cliente, id_sala: Number(sala.value),
        renglones: renglones.map((r) => ({ cod_vino: r.vino.cod_vino, cantidad: Number(r.cantidad) })),
      });
      toast(`Venta registrada: comprobante N.º ${c.nro_comprobante}.`);
      location.hash = `#/ventas/${c.nro_comprobante}`;
    } catch (e) { mostrarError(aviso, e); }
  };

  vaciar(cont).append(
    el('p', {}, el('a', { href: '#/ventas' }, '‹ Ventas')), el('h1', {}, 'Nueva venta'),
    el('form', { class: 'formulario', onsubmit: enviar },
      el('fieldset', {}, el('legend', {}, '1 · Cliente y sala'),
        buscador({ etiqueta: 'Buscar cliente (por nombre)', placeholder: 'Escriba al menos 2 letras…',
          buscar: async (t) => (await api.get('/clientes', { q: t, page_size: 8 })).items,
          describir: (c) => `${c.nombre_razon_social} · ${c.tipo_cliente}`, alElegir: (c) => { cliente = c; pintarCliente(); } }),
        cajaCliente, campo('Sala de venta', sala)),
      el('fieldset', {}, el('legend', {}, '2 · Vinos'),
        buscador({ etiqueta: 'Agregar vino', placeholder: 'Nombre del vino (2+ letras)…',
          buscar: async (t) => (await api.get('/vinos', { q: t, page_size: 8 })).items,
          describir: (v) => `${v.nombre} · ${v.anada} · stock ${v.stock_total}`,
          alElegir: (v) => { if (!renglones.some((r) => r.vino.cod_vino === v.cod_vino)) renglones.push({ vino: v, cantidad: 1 }); pintarRenglones(); } }),
        listaReng),
      el('p', { class: 'ayuda' }, 'Los precios, el descuento del cliente, los totales y el stock los calcula la base de datos al confirmar.'),
      aviso,
      el('div', { class: 'acciones' }, el('a', { class: 'btn', href: '#/ventas' }, 'Cancelar'),
        el('button', { class: 'btn btn-primario', type: 'submit', disabled: false }, 'Confirmar venta'))));
}
