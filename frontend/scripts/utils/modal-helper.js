import { escapeHtml } from './sanitize.js';

/**
 * Crear modal de edición de cantidad
 * @param {Object} item - Producto en venta
 * @param {Object} producto - Producto del catálogo
 * @param {number} precioTotal - Precio total del item
 * @returns {string} HTML del modal
 */
export function createEditModal(item, producto, precioTotal) {
  return `
    <div class="modal-overlay" id="edit-modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h2>Editar Producto</h2>
          <button class="modal-close" id="close-edit-modal">X</button>
        </div>
        <form id="edit-form" class="modal-body">
          <div class="form-group">
            <label for="producto-nombre">Nombre:</label>
            <input 
              type="text" 
              id="producto-nombre" 
              value="${escapeHtml(item.nombre)}"
              disabled
              style="background-color: #f5f5f5; cursor: not-allowed;"
            />
          </div>
          
          <div class="form-group">
            <label for="cantidad-edit">Cantidad:</label>
            <input 
              type="number" 
              id="cantidad-edit" 
              name="cantidad" 
              value="${escapeHtml(item.cantidad)}"
              min="1"
              max="${escapeHtml(producto.stock)}"
              required
            />
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="precio-unitario">Precio Unitario:</label>
              <input 
                type="text" 
                id="precio-unitario" 
                value="$${item.precio_unitario}"
                disabled
                style="background-color: #f5f5f5; cursor: not-allowed;"
              />
            </div>
            
            <div class="form-group">
              <label for="precio-total">Precio total:</label>
              <input 
                type="text" 
                id="precio-total" 
                value="$${precioTotal}"
                disabled
                style="background-color: #f5f5f5; cursor: not-allowed;"
              />
            </div>
          </div>
          
          <div class="modal-actions">
            <button type="submit" class="btn-primary">Modificar</button>
          </div>
        </form>
      </div>
    </div>
  `;
}

/**
 * Crear modal de confirmación de eliminación
 * @param {Object} item - Producto a eliminar
 * @returns {string} HTML del modal
 */
export function createConfirmDeleteModal(item) {
  const truncatedName = item.nombre.length > 50
    ? item.nombre.substring(0, 50) + '...'
    : item.nombre;

  return `
    <div class="modal-overlay" id="confirm-modal-overlay">
      <div class="modal-confirm">
        <div class="modal-icon">⚠️</div>
        <h3>¿Estas seguro de eliminar el producto <strong>${escapeHtml(truncatedName)}</strong>?</h3>
        <div class="modal-confirm-actions">
          <button class="btn-confirm-yes" id="confirm-delete">Sí</button>
          <button class="btn-confirm-no" id="cancel-delete">No</button>
        </div>
      </div>
    </div>
  `;
}

/**
 * Limpiar modales
 */
export function clearModals() {
  const modalContainer = document.getElementById('modal-container');
  if (modalContainer) {
    modalContainer.innerHTML = '';
  }
}
