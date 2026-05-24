import { fetchProductos, createVenta } from '../../services/venta-api.js';
import { showSuccess, showError, showWarning } from '../../utils/notification.js';
import { validateProductoSelected, validateCantidad, validateStockAvailable, validateVentaPreRegistro } from '../../utils/venta-validator.js';
import { displayProductos, filterProductos, clearProductoSearch } from '../../shared/producto-selector.js';
import { updateVentaTable } from '../../shared/venta-table.js';
import { initBarcodeReader } from '../../shared/barcode-reader.js';

let productosDisponibles = [];
let productosVenta = [];

/**
 * Cargar interfaz de venta de productos
 * @param {HTMLElement} container - Contenedor donde renderizar
 */
export async function loadVentaProducto(container) {
  const tpl = document.getElementById('venta-producto-template');
  container.innerHTML = '';
  
  if (!tpl) {
    container.innerHTML = '<p>Error: template de venta no encontrado.</p>';
    return;
  }

  const clone = tpl.content.cloneNode(true);
  container.appendChild(clone);

  // Inicializar
  await initVentaProducto();
}

/**
 * Inicializar lógica de venta
 */
async function initVentaProducto() {
  try {
    // Cargar productos
    productosDisponibles = await fetchProductos();
    displayProductos(productosDisponibles, productosDisponibles);

    // Configurar event listeners
    setupEventListeners();
    
    // Inicializar barcode reader
    initBarcodeReader();
  } catch (error) {
    showError('Error al inicializar venta: ' + error.message);
  }
}

/**
 * Configurar todos los event listeners
 */
function setupEventListeners() {
  const productoSearch = document.getElementById('producto-search');
  const productoDropdown = document.getElementById('producto-dropdown');
  const addBtn = document.getElementById('add-producto-btn');
  const registrarBtn = document.getElementById('registrar-venta-btn');

  if (!productoSearch || !addBtn || !registrarBtn) return;

  // Búsqueda
  productoSearch.addEventListener('input', () => filterProductos(productosDisponibles));
  
  productoSearch.addEventListener('focus', () => {
    if (!productoSearch.value) {
      displayProductos(productosDisponibles, productosDisponibles);
    }
    if (productoDropdown) productoDropdown.style.display = 'block';
  });

  // Agregar y registrar
  addBtn.addEventListener('click', handleAddProducto);
  registrarBtn.addEventListener('click', handleRegistrarVenta);

  // Cerrar dropdown al click afuera
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.form-field') && productoDropdown) {
      productoDropdown.style.display = 'none';
    }
  });
}

/**
 * Manejar agregar producto a venta
 */
function handleAddProducto() {
  const productoSearch = document.getElementById('producto-search');
  const cantidadInput = document.getElementById('cantidad-input');

  // Validar producto seleccionado
  const productoValidation = validateProductoSelected(productoSearch);
  if (!productoValidation.valid) {
    showWarning(productoValidation.message);
    return;
  }

  const productoId = parseInt(productoSearch.dataset.selectedId);
  const cantidad = parseInt(cantidadInput.value);
  const stock = parseInt(productoSearch.dataset.stock);
  const precio = parseFloat(productoSearch.dataset.precio);

  // Validar stock
  const stockValidation = validateStockAvailable(stock);
  if (!stockValidation.valid) {
    showWarning(stockValidation.message);
    return;
  }

  // Validar cantidad
  const cantidadValidation = validateCantidad(cantidad, stock);
  if (!cantidadValidation.valid) {
    showWarning(cantidadValidation.message);
    return;
  }

  // Agregar o incrementar
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

  updateVentaTable(productosVenta, productosDisponibles);
  cantidadInput.value = 1;
  clearProductoSearch();
}

/**
 * Manejar registrar venta
 */
async function handleRegistrarVenta() {
  // Validar venta
  const ventaValidation = validateVentaPreRegistro(productosVenta);
  if (!ventaValidation.valid) {
    showWarning(ventaValidation.message);
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
    await createVenta(ventaData);
    
    showSuccess('Venta registrada exitosamente');
    
    // Limpiar
    productosVenta = [];
    updateVentaTable(productosVenta, []);
    
    // Recargar productos
    productosDisponibles = await fetchProductos();
    displayProductos(productosDisponibles, productosDisponibles);
    
  } catch (error) {
    showError('Error al registrar venta: ' + error.message);
  }
}

/**
 * Exportar función global para compatibilidad
 */
window.removeProductoFromVenta = function(index) {
  productosVenta.splice(index, 1);
  updateVentaTable(productosVenta, productosDisponibles);
};
