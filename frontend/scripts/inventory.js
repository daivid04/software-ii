import { openModalForm } from "./componets/modal-product/modal-product.js";
import { renderProducts } from "./componets/product-list/product-list.js";
import { setupProductActions } from "./componets/product-list/product-actions.js";
import { loadFilterUI } from "./componets/filter-product/filter-loader.js";
import { setupFilterEvents } from "./componets/filter-product/filter-events.js";
import { initializeSearch } from "./componets/filter-product/filter-handler.js";
import { fetchFromApi } from "./data-manager.js";
import { bindBarcodeButton } from "./componets/modal-pdfcod.js";
import { loadComponent } from "./utils/component-loader.js";
import { resetBodyDefaults } from "./utils/state-manager.js";


// Limpiar caché viejo de localStorage (por si existía)
Object.keys(localStorage).forEach(key => {
  if (key.startsWith('api_cache_')) {
    localStorage.removeItem(key);
  }
});

// Cargar header y sidebar dinámicamente (Hybrid)
const headerPromise = loadComponent("header", "includes/header.html");
const sidebarPromise = loadComponent("side-bar-container", "includes/sidebar.html");
const mobileMenuPromise = loadComponent("mobile-menu-container", "includes/mobile-menu-inventory.html");

// Inicializar inventario
async function initializeInventory() {
  try {
    // 1. Cargar UI de filtros primero
    loadFilterUI();

    // 2. Configurar eventos de filtros
    setupFilterEvents();

    // 3. Mostrar skeleton loader inmediatamente
    const productList = document.getElementById("product-list");
    if (productList) {
      productList.innerHTML = `
        <div class="product-item skeleton">
          <div class="skeleton-text"></div>
          <div class="skeleton-text"></div>
          <div class="skeleton-text"></div>
          <div class="skeleton-text"></div>
          <div class="skeleton-text"></div>
          <div class="skeleton-actions"></div>
        </div>
      `.repeat(5);
    } else {
      return;
    }

    // 4. Obtener productos del servidor
    const products = await fetchFromApi('productos', null, false);

    // 5. Inicializar búsqueda con Fuse.js
    initializeSearch(products);

    // 6. Renderizar productos
    await renderProducts(products);

    // 7. Configurar acciones de productos  
    setupProductActions();

  } catch (error) {
    const productList = document.getElementById("product-list");
    if (productList) {
      productList.innerHTML = '<p class="error-state">Error al cargar productos. Por favor, recarga la página.</p>';
    }
  }
}

function setupMobileInventoryMenu() {
  // ... (código existente del menú móvil) ...
  const mobileMenu = document.querySelector("#mobile-menu-container");
  const btnList = document.getElementById("inventory-mobile-btn-list");
  const btnAdd = document.getElementById("inventory-mobile-btn-add");
  const btnBack = document.getElementById("inventory-mobile-back-btn");
  const btnBackMenu = document.querySelector(".btn-back-menu");
  const mainContent = document.querySelector(".main-content");
  const container = document.querySelector(".container");
  const safeAdd = (el, handler) => {
    if (!el) return;
    el.addEventListener("click", handler, { passive: false });
  };

  // Ver inventario
  safeAdd(btnList, () => {
    if (!mobileMenu || !mainContent || !container) return;
    mobileMenu.classList.add("hidden");
    mainContent.classList.add("active");
    container.classList.add("active");
    document.body.classList.add("inventory-open");
    document.body.classList.remove("menu-open");
    container.scrollTop = 0;
  });

  // Agregar producto
  safeAdd(btnAdd, (e) => {
    e.preventDefault();
    e.stopPropagation();

    // Ocultar menú móvil y mostrar inventario
    if (mobileMenu && mainContent) {
      mobileMenu.classList.add("hidden"); // oculta menú
      mainContent.classList.add("active"); // muestra inventario
      if (container) {
        container.classList.add("active");
      }
      document.body.classList.add("inventory-open");
      document.body.classList.remove("menu-open");
    }

    // Abrir modal
    setTimeout(() => {
      openModalForm("add");
    }, 100);
  });

  // Volver al menú
  const closeMenu = () => {
    if (!mobileMenu || !mainContent || !container) return;
    mobileMenu.classList.remove("hidden");
    mainContent.classList.remove("active");
    container.classList.remove("active");
    document.body.classList.remove("inventory-open");
    document.body.classList.add("menu-open");
    if (mobileMenu) {
      mobileMenu.style.display = '';
    }
  };

  safeAdd(btnBack, closeMenu);
  safeAdd(btnBackMenu, closeMenu);
}

// Botón agregar producto (desktop)
document.getElementById("open-modal-btn")?.addEventListener("click", (e) => {
  e.preventDefault();
  openModalForm('add');
});

// Vincular botón de códigos de barras PDF
bindBarcodeButton();

// Inicializar cuando cargue el DOM
document.addEventListener('DOMContentLoaded', async () => {
  
  // Limpiar estado previo de otros módulos
  resetBodyDefaults();
  
  // Esperar a que carguen TODOS los componentes (especialmente el menú móvil)
  await Promise.all([headerPromise, sidebarPromise, mobileMenuPromise]);
  
  document.body.classList.add("menu-open");

  // Ahora setupear el menú móvil (ya existen los elementos del DOM)
  setupMobileInventoryMenu();
  
  // Luego inicializar inventario
  await initializeInventory();

  // Abrir modal si viene desde URL
  const params = new URLSearchParams(window.location.search);
  if (params.get('open') === 'new-product') {
    openModalForm('add');
    history.replaceState(null, '', window.location.pathname);
  }
});
