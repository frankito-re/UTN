import { api } from '../api.js';
import { dinero, fecha, numero } from '../util.js';
import { campo, confirmar, el, mostrarError, opciones, paginador, tabla, toast, vaciar } from '../ui.js';

const TIPOS = ['tinto', 'blanco', 'rosado', 'espumante'];

export async function vistaCatalogo(cont, { query }) {
  const q = Object.fromEntries(query);
  const [bodegas] = await Promise.all([api.get('/bodegas')]);

  const f = {
    q: el('input', { type: 'search', name: 'q', placeholder: 'Nombre…', value: q.q || '' }),
    tipo: opciones(el('select', { name: 'tipo' }), TIPOS, (t) => t, (t) => t, 'Todos los tipos'),
    bodega: opciones(el('select', { name: 'cuit_bodega' }), bodegas, (b) => b.cuit, (b) => b.razon_social, 'Todas las bodegas'),
    pmin: el('input', { type: 'number', min: '0', step: '100', name: 'precio_min', placeholder: 'Desde', value: q.precio_min || '' }),
    pmax: el('input', { type: 'number', min: '0', step: '100', name: 'precio_max', placeholder: 'Hasta', value: q.precio_max || '' }),
    stock: opciones(el('select', { name: 'con_stock' }), [['true', 'Con stock'], ['false', 'Sin stock']], (x) => x[0], (x) => x[1], 'Cualquier stock'),
    orden: opciones(el('select', { name: 'orden' }), [['nombre', 'Nombre'], ['precio', 'Precio'], ['anada', 'Añada'], ['stock', 'Stock']], (x) => x[0], (x) => x[1]),
    sentido: opciones(el('select', { name: 'sentido' }), [['asc', 'Ascendente'], ['desc', 'Descendente']], (x) => x[0], (x) => x[1]),
  };
  f.tipo.value = q.tipo || ''; f.bodega.value = q.cuit_bodega || ''; f.stock.value = q.con_stock || '';
  f.orden.value = q.orden || 'nombre'; f.sentido.value = q.sentido || 'asc';

  const filtrar = (ev) => {
    ev.preventDefault();
    const p = new URLSearchParams();
    for (const [k, c] of [['q', f.q], ['tipo', f.tipo], ['cuit_bodega', f.bodega], ['precio_min', f.pmin], ['precio_max', f.pmax],
      ['con_stock', f.stock], ['orden', f.orden], ['sentido', f.sentido]]) if (c.value) p.set(k, c.value);
    location.hash = `#/vinos?${p}`;
  };
  const resultado = el('div', { 'aria-live': 'polite' }, el('p', { class: 'cargando' }, 'Cargando…'));

  vaciar(cont).append(
    el('div', { class: 'encabezado' }, el('h1', {}, 'Catálogo de vinos'),
      el('a', { class: 'btn btn-primario', href: '#/vinos/nuevo' }, '＋ Nuevo vino')),
    el('form', { class: 'filtros', onsubmit: filtrar },
      campo('Buscar', f.q), campo('Tipo', f.tipo), campo('Bodega', f.bodega),
      campo('Precio mín.', f.pmin), campo('Precio máx.', f.pmax), campo('Stock', f.stock),
      campo('Ordenar por', f.orden), campo('Sentido', f.sentido),
      el('button', { class: 'btn btn-primario', type: 'submit' }, 'Filtrar'),
      el('a', { class: 'btn', href: '#/vinos' }, 'Limpiar')),
    resultado);

  try {
    const pag = await api.get('/vinos', { ...q, page: q.page || 1, page_size: 15 });
    resultado.replaceChildren(
      tabla([
        { titulo: 'Vino', valor: (v) => el('strong', {}, v.nombre) },
        { titulo: 'Tipo', valor: (v) => v.tipo },
        { titulo: 'Añada', valor: (v) => v.anada },
        { titulo: 'ml', num: true, valor: (v) => numero(v.volumen_ml) },
        { titulo: 'Corte', valor: (v) => v.corte || '—' },
        { titulo: 'Bodega', valor: (v) => v.bodega },
        { titulo: 'Precio', num: true, valor: (v) => dinero(v.precio) },
        { titulo: 'Stock', num: true, valor: (v) => numero(v.stock_total) },
      ], pag.items.map((v) => ({ ...v, _alClick: () => { location.hash = `#/vinos/${v.cod_vino}`; } })),
      'Ningún vino coincide con los filtros.'),
      paginador(pag, (p) => { const n = new URLSearchParams(q); n.set('page', p); location.hash = `#/vinos?${n}`; }));
  } catch (e) { mostrarError(resultado, e); }
}

export async function vistaFicha(cont, { params }) {
  const cod = params[0];
  const zona = el('div', {}, el('p', { class: 'cargando' }, 'Cargando…'));
  vaciar(cont).append(zona);
  try {
    const [v, precios] = await Promise.all([api.get(`/vinos/${cod}`), api.get(`/vinos/${cod}/precios`)]);
    const msg = el('div', { 'aria-live': 'polite' });
    const borrar = async () => {
      if (!await confirmar('Eliminar vino', `¿Eliminar «${v.nombre}»? Solo es posible si no tiene movimientos.`, 'Eliminar')) return;
      try { await api.borrar(`/vinos/${cod}`); toast('Vino eliminado.'); location.hash = '#/vinos'; }
      catch (e) { mostrarError(msg, e); }
    };
    zona.replaceChildren(
      el('p', {}, el('a', { href: '#/vinos' }, '‹ Catálogo')),
      el('div', { class: 'encabezado' }, el('h1', {}, v.nombre),
        el('div', { class: 'acciones' },
          el('a', { class: 'btn', href: `#/vinos/${cod}/editar` }, 'Editar'),
          el('button', { class: 'btn btn-peligro', onclick: borrar }, 'Eliminar'))),
      msg,
      el('div', { class: 'grilla' },
        el('section', { class: 'tarjeta' }, el('h2', {}, 'Datos'),
          el('dl', {}, ...[['Tipo', v.tipo], ['Añada', v.anada], ['Presentación', `${v.volumen_ml} ml`],
            ['Graduación', `${v.graduacion} °`], ['Precio', dinero(v.precio)], ['Bodega', v.bodega]]
            .flatMap(([k, val]) => [el('dt', {}, k), el('dd', {}, String(val))]))),
        el('section', { class: 'tarjeta' }, el('h2', {}, 'Stock'),
          el('dl', {}, ...[['Depósito central', numero(v.stock_deposito)], ['En salas', numero(v.stock_salas)],
            ['Total', numero(v.stock_total)]].flatMap(([k, val]) => [el('dt', {}, k), el('dd', {}, val)]))),
        el('section', { class: 'tarjeta' }, el('h2', {}, 'Corte'),
          tabla([{ titulo: 'Cepa', valor: (c) => c.cepa }, { titulo: '%', num: true, valor: (c) => c.porcentaje }], v.detalle_corte)),
        el('section', { class: 'tarjeta' }, el('h2', {}, 'Maridajes'),
          v.maridajes.length ? el('ul', {}, v.maridajes.map((m) => el('li', {}, `${m.nombre} · ${m.temperatura_servicio} °C`)))
            : el('p', { class: 'vacio' }, 'Sin maridajes cargados.'))),
      el('section', { class: 'tarjeta' }, el('h2', {}, 'Historial de precios'),
        tabla([{ titulo: 'Fecha', valor: (p) => new Date(p.fecha_hora).toLocaleString('es-AR') },
          { titulo: 'Anterior', num: true, valor: (p) => dinero(p.precio_anterior) },
          { titulo: 'Nuevo', num: true, valor: (p) => dinero(p.precio_nuevo) },
          { titulo: 'Usuario', valor: (p) => p.usuario }], precios, 'Este vino nunca cambió de precio.')));
  } catch (e) { mostrarError(zona, e); }
}

export async function vistaFormVino(cont, { params }) {
  const cod = params[0];                         // undefined => alta
  const zona = el('div', {}, el('p', { class: 'cargando' }, 'Cargando…'));
  vaciar(cont).append(zona);
  try {
    const [cepas, bodegas, maridajes, actual] = await Promise.all([
      api.get('/cepas'), api.get('/bodegas'), api.get('/maridajes'), cod ? api.get(`/vinos/${cod}`) : null]);

    const c = {
      nombre: el('input', { required: true, maxlength: '80', value: actual?.nombre || '' }),
      tipo: opciones(el('select', { required: true }), TIPOS, (t) => t, (t) => t),
      anada: el('input', { type: 'number', required: true, value: actual?.anada ?? '' }),
      volumen: el('input', { type: 'number', required: true, value: actual?.volumen_ml ?? 750 }),
      graduacion: el('input', { type: 'number', step: '0.1', required: true, value: actual?.graduacion ?? '' }),
      precio: el('input', { type: 'number', step: '0.01', required: true, value: actual?.precio ?? '' }),
      bodega: opciones(el('select', { required: true }), bodegas, (b) => b.cuit, (b) => b.razon_social),
    };
    if (actual) { c.tipo.value = actual.tipo; c.bodega.value = actual.cuit_bodega; }

    const filasCorte = el('div', { class: 'filas-corte' });
    const agregarFila = (idCepa = '', pct = '') => {
      const sel = opciones(el('select', { required: true, 'aria-label': 'Cepa' }), cepas, (x) => x.id_cepa, (x) => x.nombre, 'Elegir cepa…');
      sel.value = idCepa;
      const fila = el('div', { class: 'fila-corte' }, sel,
        el('input', { type: 'number', step: '0.01', min: '0', placeholder: '%', required: true, 'aria-label': 'Porcentaje', value: pct }),
        el('button', { type: 'button', class: 'btn btn-chico', onclick: () => fila.remove(), title: 'Quitar cepa' }, '✕'));
      filasCorte.append(fila);
    };
    (actual?.detalle_corte?.length ? actual.detalle_corte : [{ id_cepa: '', porcentaje: '' }])
      .forEach((x) => agregarFila(x.id_cepa, x.porcentaje === '' ? '' : String(x.porcentaje)));

    const marcas = maridajes.map((m) => ({ m, caja: el('input', { type: 'checkbox', value: m.id_maridaje,
      checked: !!actual?.maridajes?.some((x) => x.id_maridaje === m.id_maridaje) }) }));
    const aviso = el('div', { 'aria-live': 'polite' });

    const guardar = async (ev) => {
      ev.preventDefault();
      const cuerpo = {
        nombre: c.nombre.value.trim(), tipo: c.tipo.value, anada: Number(c.anada.value), volumen_ml: Number(c.volumen.value),
        graduacion: c.graduacion.value, precio: c.precio.value, cuit_bodega: c.bodega.value,
        corte: [...filasCorte.children].map((f) => ({ id_cepa: Number(f.querySelector('select').value), porcentaje: f.querySelector('input').value })),
        maridajes: marcas.filter((x) => x.caja.checked).map((x) => x.m.id_maridaje),
      };
      try {
        const v = cod ? await api.put(`/vinos/${cod}`, cuerpo) : await api.post('/vinos', cuerpo);
        toast(cod ? 'Vino actualizado.' : 'Vino creado.');
        location.hash = `#/vinos/${v.cod_vino}`;
      } catch (e) { mostrarError(aviso, e); }
    };

    zona.replaceChildren(
      el('p', {}, el('a', { href: cod ? `#/vinos/${cod}` : '#/vinos' }, '‹ Volver')),
      el('h1', {}, cod ? `Editar «${actual.nombre}»` : 'Nuevo vino'),
      el('form', { class: 'formulario', onsubmit: guardar },
        el('div', { class: 'grilla-form' },
          campo('Nombre comercial', c.nombre), campo('Tipo', c.tipo), campo('Añada', c.anada),
          campo('Presentación (ml)', c.volumen, '375, 750 o 1500'), campo('Graduación (°)', c.graduacion, 'Entre 5 y 20'),
          campo('Precio de venta ($)', c.precio, 'Mayor que cero; único para toda la red'), campo('Bodega', c.bodega)),
        el('fieldset', {}, el('legend', {}, 'Corte (composición por cepa)'),
          el('p', { class: 'ayuda' }, 'Los porcentajes deben sumar exactamente 100: lo valida la base de datos al guardar.'),
          filasCorte, el('button', { type: 'button', class: 'btn btn-chico', onclick: () => agregarFila() }, '＋ Agregar cepa')),
        el('fieldset', {}, el('legend', {}, 'Maridajes'),
          el('div', { class: 'checks' }, marcas.map((x) => el('label', { class: 'check' }, x.caja, ` ${x.m.nombre}`)))),
        aviso,
        el('div', { class: 'acciones' }, el('a', { class: 'btn', href: cod ? `#/vinos/${cod}` : '#/vinos' }, 'Cancelar'),
          el('button', { class: 'btn btn-primario', type: 'submit' }, cod ? 'Guardar cambios' : 'Crear vino'))));
  } catch (e) { mostrarError(zona, e); }
}
