import { fetchFromApi } from "../../data-manager.js";
import { handleApiError } from "../../utils/error-handlers.js";
import { setupProductActions } from "./product-actions.js";
import { generateProductCard } from "./product-card.js";

const ENDPOINT = "productos";

/**
 * Genera HTML para skeleton loader
 */
function generateSkeletonLoader() {
  return `
    <div class="product-item skeleton">
      <div class="skeleton-text"></div>
      <div class="skeleton-text"></div>
      <div class="skeleton-text"></div>
      <div class="skeleton-text"></div>
      <div class="skeleton-text"></div>
      <div class="skeleton-actions"></div>
    </div>
  `.repeat(5); // Mostrar 5 skeleton items
}

/**
 * Renderiza la lista de productos
 * @param {Array|null} products - Productos a renderizar. Si es null, los obtiene del API.
 * @param {boolean} skipCache - Si es true, fuerza a obtener datos frescos del servidor.
 */
export async function renderProducts(products = null, skipCache = false) {
  const productList = document.getElementById("product-list");
  if (!productList) {
    return [];
  }

  try {
    // Mostrar skeleton loader solo si no tenemos productos
    if (!products) {
      productList.innerHTML = generateSkeletonLoader();
      products = await fetchFromApi(ENDPOINT, null, skipCache);
    }

    // Verificar si hay productos
    if (!products || products.length === 0) {
      productList.innerHTML = '<p class="empty-state">No hay productos registrados</p>';
      return;
    }

    // Usar DocumentFragment para renderizado eficiente
    const fragment = document.createDocumentFragment();
    const tempDiv = document.createElement('div');

    // Generar todo el HTML de una vez
    const htmlArray = products.map(producto => generateProductCard(producto));
    
    const htmlString = htmlArray.join('');
    tempDiv.innerHTML = htmlString;

    // Mover todos los nodos al fragment
    while (tempDiv.firstChild) {
      fragment.appendChild(tempDiv.firstChild);
    }

    // Una sola operación DOM
    productList.innerHTML = '';
    productList.appendChild(fragment);

    // Solo configurar acciones una vez (usa delegación de eventos)
    setupProductActions();

    return products;
  } catch (error) {
    productList.innerHTML = '<p class="error-state">Error al cargar productos</p>';
    handleApiError(error);
    return [];
  }
}