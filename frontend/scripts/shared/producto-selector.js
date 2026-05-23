import { showWarning } from '../utils/notification.js';
import { escapeHtml } from '../utils/sanitize.js';

/**
 * Mostrar lista de productos en dropdown
 * @param {Array} productos - Lista de productos
 * @param {Array} productosDisponibles - Referencia a productos disponibles
 */
export function displayProductos(productos, productosDisponibles) {
  const dropdown = document.getElementById('producto-dropdown');
  
  const itemsHTML = productos.map(p => `
    <div class="dropdown-item" 
         data-id="${escapeHtml(p.id)}" 
         data-precio="${escapeHtml(p.precioVenta)}" 
         data-stock="${escapeHtml(p.stock)}" 
         data-nombre="${escapeHtml(p.nombre)}">
      ${escapeHtml(p.nombre)} ${p.marca ? `- ${escapeHtml(p.marca)}` : ''} (Stock: ${escapeHtml(p.stock)})
    </div>
  `).join('');

  dropdown.innerHTML = itemsHTML;
  attachProductoListeners();
}

/**
 * Filtrar productos según búsqueda
 * @param {Array} productosDisponibles - Todos los productos
 */
export function filterProductos(productosDisponibles) {
  const search = document.getElementById('producto-search').value.toLowerCase();
  const dropdown = document.getElementById('producto-dropdown');

  if (!search) {
    displayProductos(productosDisponibles, productosDisponibles);
    dropdown.style.display = 'none';
    return;
  }

  const filtered = productosDisponibles.filter(p =>
    p.nombre.toLowerCase().includes(search) ||
    (p.marca && p.marca.toLowerCase().includes(search))
  );

  displayProductos(filtered, productosDisponibles);
  dropdown.style.display = 'block';
}

/**
 * Adjuntar listeners a items del dropdown
 */
function attachProductoListeners() {
  const dropdown = document.getElementById('producto-dropdown');
  
  dropdown.querySelectorAll('.dropdown-item').forEach(item => {
    item.addEventListener('click', (e) => {
      const productoSearch = document.getElementById('producto-search');
      const stock = parseInt(e.target.dataset.stock);
      const nombre = e.target.dataset.nombre;

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

/**
 * Limpiar búsqueda
 */
export function clearProductoSearch() {
  const productoSearch = document.getElementById('producto-search');
  productoSearch.value = '';
  delete productoSearch.dataset.selectedId;
  delete productoSearch.dataset.precio;
  delete productoSearch.dataset.stock;
  document.getElementById('producto-dropdown').style.display = 'none';
  productoSearch.focus();
}
