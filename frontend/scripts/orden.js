// Cargar componentes dinámicamente
import { loadComponent } from './utils/component-loader.js';
import { fetchForBarCode } from './data-manager.js';
import { showSuccess, showError, showWarning } from './utils/notification.js';
import { resetBodyDefaults } from './utils/state-manager.js';
import { escapeHtml } from './utils/sanitize.js';

// Cargar header y sidebar dinámicamente (Hybrid)
loadComponent("header", "includes/header.html");
loadComponent("side-bar-container", "includes/sidebar.html");

// Elementos del DOM
const ordenSidebar = document.getElementById('orden-sidebar');
const mainContent = document.querySelector('.main-content');
const ordenContent = document.getElementById('orden-content');


const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:8000/api/v1'  // Desarrollo local
  : '/api/v1';

// Estado del sidebar secundario
let sidebarVisible = true;

// Inicializar
document.addEventListener('DOMContentLoaded', () => {
  // Limpiar estado previo de otros módulos
  resetBodyDefaults();

  setupOrdenSidebar();
  setupSidebarToggle();

  // Mostrar el sidebar secundario por defecto al cargar la página
  showOrdenSidebar();

  // Cargar venta de producto por defecto
  loadSection('venta-producto');
  barcodeReader();
});

// Configurar eventos del sidebar secundario
function setupOrdenSidebar() {
  const menuItems = document.querySelectorAll('.orden-sidebar-menu a');

  menuItems.forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();

      // Remover clase active de todos
      menuItems.forEach(link => link.classList.remove('active'));

      // Agregar clase active al clickeado
      item.classList.add('active');

      // Obtener la sección
      const section = item.dataset.section;
      loadSection(section);
    });
  });
}

// Cargar contenido según la sección
function loadSection(section) {
  switch (section) {
    case 'venta-producto':
      loadVentaProducto();
      break;
    case 'servicios':
      ordenContent.innerHTML = `
        <h2>Servicios</h2>
        <p>Gestión de servicios...</p>
      `;
      break;
    case 'historial-servicios':
      ordenContent.innerHTML = `
        <h2>Historial de Servicios</h2>
        <p>Ver historial de servicios...</p>
      `;
      break;
    case 'pendiente':
      ordenContent.innerHTML = `
        <h2>Pendiente</h2>
        <p>Órdenes pendientes...</p>
      `;
      break;
    case 'revisado':
      ordenContent.innerHTML = `
        <h2>Revisado</h2>
        <p>Órdenes revisadas...</p>
      `;
      break;
    default:
      ordenContent.innerHTML = '<p>Selecciona una opción del menú</p>';
  }
}

// Cargar interfaz de venta de productos
async function loadVentaProducto() {
  const tpl = document.getElementById('venta-producto-template');
  ordenContent.innerHTML = '';
  if (!tpl) {
    // fallback: crear HTML mínimo si no hay template
    ordenContent.innerHTML = '<p>Error: template de venta no encontrado.</p>';
    return;
  }

  const clone = tpl.content.cloneNode(true);
  ordenContent.appendChild(clone);

  // inicializar lógica (carga productos, attach events, etc.)
  await initVentaProducto();
}

let productosDisponibles = [];
let productosVenta = [];

async function initVentaProducto() {
  // Cargar productos desde el backend
  await loadProductos();

  // Event listeners
  const productoSearch = document.getElementById('producto-search');
  const productoDropdown = document.getElementById('producto-dropdown');
  const addBtn = document.getElementById('add-producto-btn');
  const registrarBtn = document.getElementById('registrar-venta-btn');

  productoSearch.addEventListener('input', filterProductos);
  productoSearch.addEventListener('focus', () => {
    if (!productoSearch.value) {
      displayProductos(productosDisponibles);
    }
    productoDropdown.style.display = 'block';
  });

  addBtn.addEventListener('click', addProductoToVenta);
  registrarBtn.addEventListener('click', registrarVenta);

  // Ocultar dropdown al hacer click fuera
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.form-field')) {
      productoDropdown.style.display = 'none';
    }
  });
}

async function loadProductos() {
  try {
    const response = await fetch(`${API_BASE_URL}/productos/`, {
      headers: {
        'Authorization': localStorage.getItem('supabase_token') ? `Bearer ${localStorage.getItem('supabase_token')}` : ''
      }
    });
    if (!response.ok) throw new Error('Error al cargar productos');

    productosDisponibles = await response.json();
    displayProductos(productosDisponibles);
  } catch (error) {
    showError('Error al cargar productos');
  }
}

async function barcodeReader() {
  // Listener global al documento para capturar escaneos sin necesidad de focus
  let buffer = "";
  let lastTime = 0;

  document.addEventListener("keydown", async (event) => {
    // Verificar si estamos en la vista de venta (si existe el input de búsqueda)
    const reader = document.getElementById('producto-search');
    if (!reader) return;

    const currentTime = Date.now();
    const timeDiff = currentTime - lastTime;
    lastTime = currentTime;

    // Si es Enter, verificamos si tenemos un código escaneado acumulado
    if (event.key === "Enter") {
      if (buffer.length > 2) {
        event.preventDefault(); // Evitar acciones por defecto del Enter

        const barCode = buffer.replaceAll("'", "-");

        await processScannedProduct(barCode, reader);

        buffer = ""; // Limpiar buffer tras procesar
      } else {
        buffer = ""; // Enter manual o buffer sucio
      }
      return;
    }

    // Ignorar teclas especiales (Shift, Ctrl, Alt, etc.)
    if (event.key.length > 1) return;

    // Lógica de detección de escáner basada en velocidad (< 60ms entre teclas)
    if (timeDiff < 60) {
      // Ráfaga detectada: Es el lector de códigos
      event.preventDefault(); // Evitar que se escriba en cualquier input activo

      // Corrección del primer carácter:
      // El primer carácter del código siempre llega "lento" (timeDiff alto).
      // Si el foco estaba en un input, ese carácter se escribió. Aquí intentamos borrarlo.
      if (buffer.length === 1 && document.activeElement.tagName === 'INPUT') {
        const input = document.activeElement;
        // Verificamos si el input termina con ese carácter para borrarlo con seguridad
        if (input.value.endsWith(buffer)) {
          input.value = input.value.slice(0, -1);
        }
      }

      buffer += event.key;
    } else {
      // Tiempo largo: Puede ser escritura manual o el PRIMER carácter de un escaneo
      // Lo guardamos en el buffer por si acaso, pero dejamos que se escriba (no preventDefault)
      buffer = event.key;
    }
  });
}

async function processScannedProduct(barCode, reader) {
  try {
    const producto = await fetchForBarCode(barCode);

    if (!producto) {
      showWarning(`Producto no encontrado: ${barCode}`);
      return;
    }

    if (producto.stock === 0) {
      showWarning(`Sin stock: ${producto.nombre}`);
      return;
    }

    // Llenar datos
    reader.value = producto.nombre;
    reader.dataset.selectedId = producto.id;
    reader.dataset.precio = producto.precioVenta;
    reader.dataset.stock = producto.stock;

    // Asegurar que el dropdown esté cerrado (ya que es una selección automática)
    const dropdown = document.getElementById('producto-dropdown');
    if (dropdown) dropdown.style.display = 'none';

    showSuccess(`Producto detectado: ${producto.nombre}`);

    // Mover foco a cantidad
    const cantidadInput = document.getElementById('cantidad-input');
    if (cantidadInput) {
      cantidadInput.value = 1;
      cantidadInput.focus();
      cantidadInput.select();
    }

  } catch (error) {
    showError('Error al procesar código de barras');
  }
}

function displayProductos(productos) {
  const dropdown = document.getElementById('producto-dropdown');
  const itemsHTML = productos.map(p => `
    <div class="dropdown-item" data-id="${escapeHtml(p.id)}" data-precio="${escapeHtml(p.precioVenta)}" data-stock="${escapeHtml(p.stock)}" data-nombre="${escapeHtml(p.nombre)}">
      ${escapeHtml(p.nombre)} ${p.marca ? `- ${escapeHtml(p.marca)}` : ''} (Stock: ${escapeHtml(p.stock)})
    </div>
  `).join('');

  dropdown.innerHTML = itemsHTML;

  // Agregar event listeners a cada item
  dropdown.querySelectorAll('.dropdown-item').forEach(item => {
    item.addEventListener('click', (e) => {
      const productoSearch = document.getElementById('producto-search');
      const stock = parseInt(e.target.dataset.stock);
      const nombre = e.target.dataset.nombre;

      // Validar stock antes de seleccionar
      if (stock === 0) {
        showWarning('Este producto no tiene stock disponible');
        dropdown.style.display = 'none';
        productoSearch.value = '';
        return;
      }

      productoSearch.value = nombre;
      productoSearch.dataset.selectedId = e.target.dataset.id;
      productoSearch.dataset.precio = e.target.dataset.precio;
      productoSearch.dataset.stock = e.target.dataset.stock;
      dropdown.style.display = 'none';
    });
  });
}

function filterProductos() {
  const search = document.getElementById('producto-search').value.toLowerCase();
  const dropdown = document.getElementById('producto-dropdown');

  if (!search) {
    displayProductos(productosDisponibles);
    dropdown.style.display = 'none';
    return;
  }

  const filtered = productosDisponibles.filter(p =>
    p.nombre.toLowerCase().includes(search) ||
    p.marca.toLowerCase().includes(search)
  );

  displayProductos(filtered);
  dropdown.style.display = 'block';
}

function addProductoToVenta() {
  const productoSearch = document.getElementById('producto-search');
  const cantidadInput = document.getElementById('cantidad-input');

  if (!productoSearch.dataset.selectedId) {
    showWarning('Selecciona un producto');
    return;
  }

  const productoId = parseInt(productoSearch.dataset.selectedId);
  const cantidad = parseInt(cantidadInput.value);
  const stock = parseInt(productoSearch.dataset.stock);
  const precio = parseInt(productoSearch.dataset.precio);

  if (cantidad <= 0) {
    showWarning('La cantidad debe ser mayor a 0');
    return;
  }

  if (stock === 0) {
    showWarning('Este producto no tiene stock disponible');
    return;
  }

  if (cantidad > stock) {
    showWarning(`Stock insuficiente. Disponible: ${stock}`);
    return;
  }

  // Verificar si el producto ya está en la venta
  const existingIndex = productosVenta.findIndex(p => p.producto_id === productoId);
  if (existingIndex >= 0) {
    productosVenta[existingIndex].cantidad += cantidad;
  } else {
    const producto = productosDisponibles.find(p => p.id === productoId);
    productosVenta.push({
      producto_id: productoId,
      nombre: producto.nombre,
      cantidad: cantidad,
      precio_unitario: precio
    });
  }

  updateVentaTable();
  cantidadInput.value = 1;

  // Limpiar búsqueda
  document.getElementById('producto-search').value = '';
  delete productoSearch.dataset.selectedId;
  delete productoSearch.dataset.precio;
  delete productoSearch.dataset.stock;
  document.getElementById('producto-dropdown').style.display = 'none';
  productoSearch.focus();
}

function updateVentaTable() {
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

  // Agregar event listeners a los botones
  attachTableEvents();
}

function attachTableEvents() {
  // Botones de editar
  document.querySelectorAll('.btn-edit').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const index = parseInt(e.currentTarget.dataset.index);
      editCantidad(index);
    });
  });

  // Botones de eliminar
  document.querySelectorAll('.btn-delete').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const index = parseInt(e.currentTarget.dataset.index);
      removeProductoFromVenta(index);
    });
  });
}

function editCantidad(index) {
  const item = productosVenta[index];
  const producto = productosDisponibles.find(p => p.id === item.producto_id);

  const modalContainer = document.getElementById('modal-container');
  if (!modalContainer) return;

  const precioTotal = item.cantidad * item.precio_unitario;

  modalContainer.innerHTML = `
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

  // Event listeners del modal
  const closeBtn = document.getElementById('close-edit-modal');
  const overlay = document.getElementById('edit-modal-overlay');
  const form = document.getElementById('edit-form');
  const cantidadInput = document.getElementById('cantidad-edit');
  const precioTotalInput = document.getElementById('precio-total');

  // Actualizar precio total cuando cambia la cantidad
  if (cantidadInput) {
    cantidadInput.addEventListener('input', () => {
      const nuevaCantidad = parseInt(cantidadInput.value) || 0;
      const nuevoTotal = nuevaCantidad * item.precio_unitario;
      precioTotalInput.value = `$${nuevoTotal}`;
    });
  }

  if (closeBtn) {
    closeBtn.addEventListener('click', closeModal);
  }

  if (overlay) {
    overlay.addEventListener('click', (e) => {
      if (e.target.id === 'edit-modal-overlay') closeModal();
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
      updateVentaTable();
      showSuccess('Cantidad actualizada');
      closeModal();
    });
  }
}

function removeProductoFromVenta(index) {
  const item = productosVenta[index];

  const modalContainer = document.getElementById('modal-container');
  if (!modalContainer) return;

  // Truncar nombre si es muy largo
  const truncatedName = item.nombre.length > 50
    ? item.nombre.substring(0, 50) + '...'
    : item.nombre;

  modalContainer.innerHTML = `
    <div class="modal-overlay" id="confirm-modal-overlay">
      <div class="modal-confirm">
        <div class="modal-icon">⚠️</div>
        <h3>¿Estas seguro de eliminar el producto <strong>${truncatedName}</strong>?</h3>
        <div class="modal-confirm-actions">
          <button class="btn-confirm-yes" id="confirm-delete">Sí</button>
          <button class="btn-confirm-no" id="cancel-delete">No</button>
        </div>
      </div>
    </div>
  `;

  document.getElementById('confirm-delete').addEventListener('click', () => {
    productosVenta.splice(index, 1);
    updateVentaTable();
    showSuccess('Producto eliminado de la venta');
    closeModal();
  });

  document.getElementById('cancel-delete').addEventListener('click', closeModal);
  document.getElementById('confirm-modal-overlay').addEventListener('click', (e) => {
    if (e.target.id === 'confirm-modal-overlay') closeModal();
  });
}

function closeModal() {
  const modalContainer = document.getElementById('modal-container');
  if (modalContainer) modalContainer.innerHTML = '';
}

async function registrarVenta() {
  if (productosVenta.length === 0) {
    showWarning('Agrega al menos un producto a la venta');
    return;
  }

  const ventaData = {
    fecha: new Date().toISOString(),
    productos: productosVenta.map(p => ({
      producto_id: p.producto_id,
      cantidad: p.cantidad
    }))
  };

  try {
    const response = await fetch(`${API_BASE_URL}/ventas/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': localStorage.getItem('supabase_token') ? `Bearer ${localStorage.getItem('supabase_token')}` : ''
      },
      body: JSON.stringify(ventaData)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Error al registrar venta');
    }

    showSuccess('Venta registrada exitosamente');

    // Limpiar la venta
    productosVenta = [];
    updateVentaTable();

    // Recargar productos para actualizar stock
    await loadProductos();

  } catch (error) {
    showError('Error al registrar venta: ' + error.message);
  }
}

// Exponer función globalmente para el onclick
window.removeProductoFromVenta = removeProductoFromVenta;

// Configurar toggle del sidebar desde el menú principal
function setupSidebarToggle() {
  // Escuchar clicks en el botón "Orden" del sidebar principal
  document.addEventListener('click', (e) => {
    const ordenLink = e.target.closest('a[href="orden.html"]');

    if (ordenLink && window.location.pathname.includes('orden.html')) {
      e.preventDefault();
      toggleOrdenSidebar();
    }
  });
}

// Mostrar/ocultar sidebar secundario
function toggleOrdenSidebar() {
  sidebarVisible = !sidebarVisible;

  if (sidebarVisible) {
    showOrdenSidebar();
  } else {
    hideOrdenSidebar();
  }
}

function showOrdenSidebar() {
  ordenSidebar.classList.remove('hidden');
  mainContent.classList.add('with-orden-sidebar');
  sidebarVisible = true;
}

function hideOrdenSidebar() {
  ordenSidebar.classList.add('hidden');
  mainContent.classList.remove('with-orden-sidebar');
  sidebarVisible = false;
}

// Exportar funciones si se necesitan
export { toggleOrdenSidebar, loadSection };
