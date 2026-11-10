// Funciones puras (sin DOM): se pueden probar con `node --test front/test`.

/** Arma "?a=1&b=2" omitiendo valores vacios. Todo se codifica: nunca se concatena texto crudo. */
export function armarQuery(params = {}) {
  const usp = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    if (v === undefined || v === null || v === '' || v === false) continue;
    usp.append(k, String(v));
  }
  const s = usp.toString();
  return s ? `?${s}` : '';
}

/** Traduce el cuerpo de error de la API ({error:{estado,sqlstate,mensaje,regla,detalle}}) a algo mostrable. */
export function describirError(estado, cuerpo) {
  const e = cuerpo && cuerpo.error ? cuerpo.error : {};
  const titulos = {
    400: 'Datos inválidos', 403: 'Operación no permitida', 404: 'No encontrado',
    409: 'Conflicto', 422: 'No cumple una regla del negocio', 503: 'Servicio no disponible',
  };
  return {
    estado,
    titulo: titulos[estado] || (estado >= 500 ? 'Error del servidor' : 'Error'),
    mensaje: e.mensaje || 'No se pudo completar la operación.',
    regla: e.regla || null,
    detalle: Array.isArray(e.detalle) ? e.detalle.map((d) => `${d.campo}: ${d.problema}`) : [],
  };
}

const moneda = new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS', maximumFractionDigits: 2 });
const entero = new Intl.NumberFormat('es-AR');

/** Solo formatea para mostrar un valor que YA calculo la base; no hace cuentas. */
export const dinero = (n) => (n === null || n === undefined ? '—' : moneda.format(n));
export const numero = (n) => (n === null || n === undefined ? '—' : entero.format(n));
export const fecha = (iso) => {
  if (!iso) return '—';
  const [a, m, d] = String(iso).slice(0, 10).split('-');
  return `${d}/${m}/${a}`;
};

export const ESTADOS = { en_confeccion: 'En confección', terminado: 'Terminado', procesado: 'Procesado' };
export const etiquetaEstado = (e) => ESTADOS[e] || e;

/** Pagina las paginas a mostrar en el paginador (maximo 7 botones, con huecos). */
export function paginasVisibles(actual, total) {
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1);
  const set = new Set([1, total, actual, actual - 1, actual + 1, actual - 2, actual + 2]);
  const orden = [...set].filter((p) => p >= 1 && p <= total).sort((a, b) => a - b);
  const out = [];
  orden.forEach((p, i) => {
    if (i && p - orden[i - 1] > 1) out.push('…');
    out.push(p);
  });
  return out;
}

/** Ruta del hash: '#/vinos/12/editar' -> {ruta:'/vinos/12/editar', query:URLSearchParams} */
export function parsearHash(hash) {
  const limpio = (hash || '').replace(/^#/, '') || '/vinos';
  const [ruta, qs = ''] = limpio.split('?');
  return { ruta, query: new URLSearchParams(qs) };
}
