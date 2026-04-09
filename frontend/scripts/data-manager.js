import { handleApiError } from "./utils/error-handlers.js";

/**
 * URL base para la API
 * @constant {string}
 */
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:8000/api/v1'  // Desarrollo local
  : '/api/v1';

const token = localStorage.getItem('supabase_token');

// ========================================
// SIN CACHÉ - DATOS SIEMPRE FRESCOS
// ========================================
// Mantener función vacía para compatibilidad
export function invalidateCache(endpoint) {
  // No hace nada, ya no hay caché
}

// ========================================
// FUNCIONES GENÉRICAS
// ========================================

/**
 * Realiza peticiones GET a la API - SIEMPRE datos frescos del servidor.
 * @param {string} endpoint - Ruta del endpoint (ej: 'productos', 'autopartes').
 * @param {number|null} id - ID opcional para obtener un recurso específico.
 * @param {boolean} skipCache - Parámetro mantenido por compatibilidad (no se usa).
 * @returns {Promise<Object|Array>} Datos de la respuesta en formato JSON.
 * @throws {Error} Si la petición falla.
 */
export async function fetchFromApi(endpoint, id = null, skipCache = false) {
  try {
    let apiUrl = `${API_BASE_URL}/${endpoint}/`;
    if (id !== null) {
      apiUrl = `${API_BASE_URL}/${endpoint}/${id}`;
    }
    
    // Añadir timestamp para evitar caché del navegador
    const separator = apiUrl.includes('?') ? '&' : '?';
    apiUrl += `${separator}_t=${Date.now()}`;

    // Siempre hacer petición al API sin caché del navegador
    const response = await fetch(apiUrl, {
      method: 'GET',
      headers: {
        'Authorization': token ? `Bearer ${token}` : '',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
      }
    });
    checkResponseStatus(response);

    const data = await response.json();
    return data;
    
  } catch (error) {
    handleApiError(error, {
      endpoint,
      method: 'GET',
      id,
    });
  }
}

/**
 * Crea un recurso en la API mediante POST.
 * @param {string} endpoint - Ruta del endpoint.
 * @param {Object} data - Datos a enviar en el body.
 * @returns {Promise<Object>} Recurso creado.
 * @throws {Error} Si la petición falla.
 */
export async function createResource(endpoint, data) {
  try {
    const response = await fetch(`${API_BASE_URL}/${endpoint}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : '',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      let errorData = null;
      try {
        errorData = await response.json();
      } catch (e) {
        // Si no se puede parsear, ignorar
      }
      
      const error = new Error(errorData?.detail || `Error HTTP: ${response.status}`);
      error.status = response.status;
      error.detail = errorData?.detail;
      throw error;
    }

    const result = await response.json();
    return result;
  } catch (error) {
    handleApiError(error, {
      endpoint,
      method: 'POST',
      data,
    });
  }
}

/**
 * Actualiza un recurso en la API mediante PUT.
 * @param {string} endpoint - Ruta del endpoint.
 * @param {number} id - ID del recurso a actualizar.
 * @param {Object} data - Datos actualizados en formato JSON.
 * @returns {Promise<Object>} Recurso actualizado.
 * @throws {Error} Si la petición falla.
 */
export async function updateResource(endpoint, id, data) {
  try {
    const response = await fetch(`${API_BASE_URL}/${endpoint}/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : '',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      let errorData = null;
      try {
        errorData = await response.json();
      } catch (e) {
        // Si no se puede parsear, ignorar
      }
      
      const error = new Error(errorData?.detail || `Error HTTP: ${response.status}`);
      error.status = response.status;
      error.detail = errorData?.detail;
      throw error;
    }

    const result = await response.json();
    return result;
  } catch (error) {
    handleApiError(error, {
      endpoint,
      method: 'PUT',
      id,
      data,
    });
  }
}

/**
 * Elimina un recurso de la API mediante DELETE.
 * @param {string} endpoint - Ruta del endpoint.
 * @param {number} id - ID del recurso a eliminar.
 * @returns {Promise<Object>} Respuesta del servidor.
 * @throws {Error} Si la petición falla.
 */
export async function deleteResource(endpoint, id) {
  try {
    const response = await fetch(`${API_BASE_URL}/${endpoint}/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': token ? `Bearer ${token}` : '',
      },
    });

    // Si la respuesta no es ok, intentar leer el JSON de error
    if (!response.ok) {
      let errorData = null;
      try {
        const text = await response.text();
        errorData = text ? JSON.parse(text) : null;
      } catch (e) {
        // Si no se puede parsear, ignorar
      }
      
      const error = new Error(errorData?.detail || `Error HTTP: ${response.status}`);
      error.status = response.status;
      error.detail = errorData?.detail;
      throw error;
    }

    let result = null;
    if (response.status !== 204) {
      const text = await response.text();
      result = text ? JSON.parse(text) : null;
    }

    return result;
  } catch (error) {
    handleApiError(error, {
      endpoint,
      method: 'DELETE',
      id,
    });
  }
}

/**
 * Cuenta elementos de un endpoint.
 * @param {string} endpoint - Ruta del endpoint a contar elementos.
 * @returns {Promise<number>} Cantidad de elementos.
 */
export async function countFromApi(endpoint) {
  try {
    const object = await fetchFromApi(endpoint, null, true);
    if (!Array.isArray(object)) {
      return 0;
    }
    return object.length;
  } catch (error) {
    handleApiError(error, {
      endpoint,
      method: 'GET',
    });
    return 0;
  }
}

// ========================================
// FUNCIONES ESPECÍFICAS - PRODUCTOS
// (Provisionales hasta implementación en backend)
// ========================================

/**
 * Cuenta productos con stock menor o igual al mínimo.
 * @returns {Promise<number>} Cantidad de productos en bajo stock.
 */
export async function productUnderStock() {
  try {
    const products = await fetchFromApi('productos');
    const amount = products.reduce((count, product) => {
      return count + (product.stock <= product.stockMin ? 1 : 0);
    }, 0);

    return amount;
  } catch (error) {
    handleApiError(error, {
      endpoint: 'productos',
      method: 'GET',
    });
    return 0;
  }
}

/**
 * Verifica el estado de la respuesta HTTP y lanza error si no es exitosa.
 * @param {Response} response - Objeto Response de fetch.
 * @throws {Error} Error con status HTTP si la respuesta no es exitosa.
 */
function checkResponseStatus(response) {
  if (!response.ok) {
    const error = new Error(`Error HTTP: ${response.status}`);
    error.status = response.status;
    throw error;
  }
}

export async function fetchForBarCode(barCode) {
  try {
    const response = await fetch(`${API_BASE_URL}/productos/barcode/${barCode}`, {
      headers: {
        'Authorization': token ? `Bearer ${token}` : '',
      }
    });

    if (!response.ok) {
      if (response.status === 404) {
        return null; // Producto no encontrado
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const product = await response.json();
    return product;
  } catch (error) {
    handleApiError(error);
    return null;
  }
}