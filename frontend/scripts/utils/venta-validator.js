/**
 * Validar que un producto esté seleccionado
 * @param {HTMLElement} productoSearch - Input de búsqueda
 * @returns {Object} { valid: boolean, message: string }
 */
export function validateProductoSelected(productoSearch) {
  if (!productoSearch.dataset.selectedId) {
    return { valid: false, message: 'Selecciona un producto' };
  }
  return { valid: true };
}

/**
 * Validar cantidad ingresada
 * @param {number} cantidad - Cantidad a validar
 * @param {number} stock - Stock disponible
 * @returns {Object} { valid: boolean, message: string }
 */
export function validateCantidad(cantidad, stock) {
  if (cantidad <= 0) {
    return { valid: false, message: 'La cantidad debe ser mayor a 0' };
  }
  if (cantidad > stock) {
    return { valid: false, message: `Stock insuficiente. Disponible: ${stock}` };
  }
  return { valid: true };
}

/**
 * Validar stock disponible
 * @param {number} stock - Stock a validar
 * @returns {Object} { valid: boolean, message: string }
 */
export function validateStockAvailable(stock) {
  if (stock === 0) {
    return { valid: false, message: 'Este producto no tiene stock disponible' };
  }
  return { valid: true };
}

/**
 * Validar cantidad para edición
 * @param {number} nuevaCantidad - Nueva cantidad
 * @param {number} stock - Stock disponible
 * @returns {Object} { valid: boolean, message: string }
 */
export function validateEditCantidad(nuevaCantidad, stock) {
  if (isNaN(nuevaCantidad) || nuevaCantidad <= 0) {
    return { valid: false, message: 'La cantidad debe ser un número mayor a 0' };
  }
  if (nuevaCantidad > stock) {
    return { valid: false, message: `Stock insuficiente. Disponible: ${stock}` };
  }
  return { valid: true };
}

/**
 * Validar venta antes de registrar
 * @param {Array} productosVenta - Productos en la venta
 * @returns {Object} { valid: boolean, message: string }
 */
export function validateVentaPreRegistro(productosVenta) {
  if (productosVenta.length === 0) {
    return { valid: false, message: 'Agrega al menos un producto a la venta' };
  }
  return { valid: true };
}
