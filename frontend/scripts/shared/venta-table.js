import { escapeHtml } from '../utils/sanitize.js';
import { showSuccess, showWarning } from '../utils/notification.js';
import { createEditModal, createConfirmDeleteModal, clearModals } from '../utils/modal-helper.js';

/**
 * Renderizar tabla de productos en venta
 * @param {Array} productosVenta - Productos agregados a la venta
 * @param {Array} productosDisponibles - Catálogo de productos
 */
export function updateVentaTable(productosVenta, productosDisponibles) {
  const tbody = document.getElementById('productos-table-body');

  tbody.innerHTML = productosVenta.map((item, index) => `
    <div class="table-row" data-index="${index}">
      <div class="table-cell">${escapeHtml(item.nombre)}</div>
      <div class="table-cell editable-cantidad" data-index="${index}">${escapeHtml(item.cantidad)}</div>
      <div class="table-cell">$${escapeHtml(item.precio_unitario)}</div>
      <div class="table-cell">$${escapeHtml(item.cantidad * item.precio_unitario)}</div>
      <div class="table-cell table-actions">
        <button class="btn-edit" data-index="${index}" title="Editar">
          <img class="img-edit" src="../assets/icons/edit.png" alt="Editar">
        </button>
        <button class="btn-delete" data-index="${index}" title="Eliminar">
          <img class="img-delete" src="../assets/icons/delete.png" alt="Eliminar">
        </button>
      </div>
    </div>
  `).join('');

  // Calcular total
  const total = productosVenta.reduce((sum, item) =>
    sum + (item.cantidad * item.precio_unitario), 0
  );
  document.getElementById('total-venta').textContent = `$${total}`;

  // Adjuntar eventos
  attachTableEvents(productosVenta, productosDisponibles);
}

/**
 * Adjuntar eventos a botones de la tabla
 */
function attachTableEvents(productosVenta, productosDisponibles) {
  document.querySelectorAll('.btn-edit').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const index = parseInt(e.currentTarget.dataset.index);
      openEditModal(index, productosVenta, productosDisponibles);
    });
  });

  document.querySelectorAll('.btn-delete').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const index = parseInt(e.currentTarget.dataset.index);
      openDeleteModal(index, productosVenta);
    });
  });
}

/**
 * Abrir modal de edición
 */
function openEditModal(index, productosVenta, productosDisponibles) {
  const item = productosVenta[index];
  const producto = productosDisponibles.find(p => p.id === item.producto_id);

  if (!producto) return;

  const modalContainer = document.getElementById('modal-container');
  if (!modalContainer) return;

  const precioTotal = item.cantidad * item.precio_unitario;
  modalContainer.innerHTML = createEditModal(item, producto, precioTotal);

  const closeBtn = document.getElementById('close-edit-modal');
  const overlay = document.getElementById('edit-modal-overlay');
  const form = document.getElementById('edit-form');
  const cantidadInput = document.getElementById('cantidad-edit');
  const precioTotalInput = document.getElementById('precio-total');

  // Actualizar precio en tiempo real
  if (cantidadInput) {
    cantidadInput.addEventListener('input', () => {
      const nuevaCantidad = parseInt(cantidadInput.value) || 0;
      const nuevoTotal = nuevaCantidad * item.precio_unitario;
      precioTotalInput.value = `$${nuevoTotal}`;
    });
  }

  if (closeBtn) {
    closeBtn.addEventListener('click', clearModals);
  }

  if (overlay) {
    overlay.addEventListener('click', (e) => {
      if (e.target.id === 'edit-modal-overlay') clearModals();
    });
  }

  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const nuevaCantidad = parseInt(document.getElementById('cantidad-edit').value);

      if (isNaN(nuevaCantidad) || nuevaCantidad <= 0) {
        showWarning('La cantidad debe ser un número mayor a 0');
        return;
      }

      if (nuevaCantidad > producto.stock) {
        showWarning(`Stock insuficiente. Disponible: ${producto.stock}`);
        return;
      }

      productosVenta[index].cantidad = nuevaCantidad;
      updateVentaTable(productosVenta, productosDisponibles);
      showSuccess('Cantidad actualizada');
      clearModals();
    });
  }
}

/**
 * Abrir modal de confirmación de eliminación
 */
function openDeleteModal(index, productosVenta) {
  const item = productosVenta[index];
  const modalContainer = document.getElementById('modal-container');
  if (!modalContainer) return;

  modalContainer.innerHTML = createConfirmDeleteModal(item);

  document.getElementById('confirm-delete').addEventListener('click', () => {
    productosVenta.splice(index, 1);
    updateVentaTable(productosVenta, []);
    showSuccess('Producto eliminado de la venta');
    clearModals();
  });

  document.getElementById('cancel-delete').addEventListener('click', clearModals);
  document.getElementById('confirm-modal-overlay').addEventListener('click', (e) => {
    if (e.target.id === 'confirm-modal-overlay') clearModals();
  });
}
