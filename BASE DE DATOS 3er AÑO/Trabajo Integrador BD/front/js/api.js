import { armarQuery, describirError } from './util.js';

const BASE = (typeof window !== 'undefined' && window.API_BASE) || '/api';

export class ErrorApi extends Error {
  constructor(info) {
    super(info.mensaje);
    this.info = info;
  }
}

async function pedir(metodo, ruta, { query, cuerpo } = {}) {
  let resp;
  try {
    resp = await fetch(`${BASE}${ruta}${armarQuery(query)}`, {
      method: metodo,
      headers: cuerpo !== undefined ? { 'Content-Type': 'application/json' } : {},
      body: cuerpo !== undefined ? JSON.stringify(cuerpo) : undefined,
    });
  } catch {
    throw new ErrorApi(describirError(503, { error: { mensaje: 'No hay conexión con el servidor.' } }));
  }
  if (resp.status === 204) return null;
  let datos = null;
  try { datos = await resp.json(); } catch { /* cuerpo vacio o no JSON */ }
  if (!resp.ok) throw new ErrorApi(describirError(resp.status, datos));
  return datos;
}

export const api = {
  get: (ruta, query) => pedir('GET', ruta, { query }),
  post: (ruta, cuerpo) => pedir('POST', ruta, { cuerpo: cuerpo ?? {} }),
  put: (ruta, cuerpo) => pedir('PUT', ruta, { cuerpo }),
  borrar: (ruta) => pedir('DELETE', ruta),
};
