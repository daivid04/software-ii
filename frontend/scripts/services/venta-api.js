// Configuración de API
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:8000/api/v1'
  : '/api/v1';

// Obtener token de autenticación
function getAuthHeader() {
  const token = localStorage.getItem('supabase_token');
  return token ? { 'Authorization': `Bearer ${token}` } : {};
}

/**
 * Cargar lista de productos disponibles
 * @returns {Promise<Array>} Lista de productos
 */
export async function fetchProductos() {
  const response = await fetch(`${API_BASE_URL}/productos/`, {
    headers: getAuthHeader()
  });
  
  if (!response.ok) {
    throw new Error('Error al cargar productos');
  }
  
  return await response.json();
}

/**
 * Buscar producto por código de barras
 * @param {string} barCode - Código de barras
 * @returns {Promise<Object>} Producto encontrado
 */
export async function fetchProductoByBarCode(barCode) {
  const response = await fetch(`${API_BASE_URL}/productos/barcode/${barCode}`, {
    headers: getAuthHeader()
  });
  
  if (!response.ok) {
    return null;
  }
  
  return await response.json();
}

/**
 * Registrar una nueva venta
 * @param {Object} ventaData - Datos de la venta
 * @returns {Promise<Object>} Venta creada
 */
export async function createVenta(ventaData) {
  const response = await fetch(`${API_BASE_URL}/ventas/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeader()
    },
    body: JSON.stringify(ventaData)
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Error al registrar venta');
  }

  return await response.json();
}

export { API_BASE_URL };
