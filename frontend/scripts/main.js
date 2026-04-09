// main.js
// Script principal que manipula el DOM y obtiene datos dinámicos desde data-manager.js
// Todas las funciones y textos están documentados en español.

import { productUnderStock, countFromApi } from './data-manager.js';
import { bindAddProductButton } from './componets/modal-product/modal-product.js';
// ========================================
// HELPERS DE DOM
// ========================================

const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

// ========================================
// SELECTORES DEL DOM
// ========================================

const selectors = {
  cards: '.dashboard-card-grid .card',
  quickActionsList: '.quick-actions .list-action',
};

// ========================================
// FUNCIONES DE RENDERIZADO
// ========================================

/**
 * Renderiza la alerta de productos con bajo stock
 * @param {number} count - Cantidad de productos con bajo stock
 */
function renderAlert(count) {
  const alertContent = $('.welcome-alert .alert-content');
  if (!alertContent) {
    return;
  }

  // Limpiar el contenido anterior
  alertContent.innerHTML = '';

  if (count > 0) {
    // Crear elementos dinámicamente
    const h3 = document.createElement('h3');
    h3.textContent = `¡Hay ${count} producto${count > 1 ? 's' : ''} por agotarse!`;

    const link = document.createElement('a');
    link.textContent = 'Ver productos';
    link.href = '#/inventario';

    alertContent.appendChild(h3);
    alertContent.appendChild(link);

  } else {
    const h3 = document.createElement('h3');
    h3.textContent = '✅ Todos los productos tienen stock suficiente.';
    alertContent.appendChild(h3);

  }
}

/**
 * Renderiza una tarjeta del dashboard
 * @param {HTMLElement} card - Elemento de la tarjeta
 * @param {string} title - Título de la tarjeta
 * @param {number} value - Valor numérico a mostrar
 */
function renderCard(card, title, value) {
  if (!card) {
    return;
  }


  const titleEl = $('h3', card);
  const valueEl = $('p', card);

  if (titleEl) titleEl.textContent = title;
  if (valueEl) {
    const icon = valueEl.querySelector('img');
    valueEl.textContent = `${value} `;
    if (icon) valueEl.appendChild(icon);
  }

}

/**
 * Renderiza todas las tarjetas del dashboard con datos de la BD
 */
async function renderCards() {
  const cards = $$(selectors.cards);
  if (!cards.length) return;

  // Tarjeta 0: Productos en inventario
  try {
    const productCount = await countFromApi('productos');
    renderCard(cards[0], 'Productos en inventario', productCount);
  } catch (error) {
    renderCard(cards[0], 'Productos en inventario', 0);
  }

  // Tarjeta 1: Ventas recientes (mantener estático por ahora)
  try {
    const titleEl = $('h3', cards[1]);
    if (titleEl) titleEl.textContent = 'Ventas recientes';
  } catch (error) {
  }

  // Tarjeta 2: Servicios activos
  try {
    const serviciosCount = await countFromApi('servicios');
    renderCard(cards[2], 'Servicios activos', serviciosCount);
  } catch (error) {
    renderCard(cards[2], 'Servicios activos', 0);
  }
}

/**
 * Vincula eventos a las acciones rápidas
 */
function bindQuickActions() {
  const list = $(selectors.quickActionsList);
  if (!list) return;

  list.addEventListener('click', (ev) => {
    const li = ev.target.closest('li');
    if (!li) return;
    const text = li.textContent.trim();
    // TODO: Implementar navegación o modales según la acción
  });
}

// ========================================
// INICIALIZACIÓN
// ========================================

/**
 * Inicializa el dashboard cargando todos los datos
 */
async function init() {
  try {
    // 1. Vincular eventos
    bindQuickActions();

    // 2. Cargar y renderizar alerta de bajo stock
    const lowStockCount = await productUnderStock();
    renderAlert(lowStockCount);

    // 3. Cargar y renderizar tarjetas
    await renderCards();


  } catch (error) {
  }
}

// Iniciar cuando el DOM esté listo
// Iniciar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', async () => {
  // Cargar componentes dinámicamente (si no están ya cargados por SSI)
  const { loadComponent } = await import('./utils/component-loader.js');
  await loadComponent("header", "includes/header.html");
  await loadComponent("side-bar", "includes/sidebar.html");

  init();
});
