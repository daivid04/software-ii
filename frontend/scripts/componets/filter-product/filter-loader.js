import { CATEGORIAS_PRODUCTOS } from "../modal-product/constants.js";

export function loadFilterUI() {
  const categoryContainer = document.querySelector('.category-option');
  if (!categoryContainer) return;

  // Generar checkboxes (desktop)
  const checkboxesHTML = CATEGORIAS_PRODUCTOS.map(categoria => `
    <li>
      <label>
        <input type="checkbox" name="category" value="${categoria}">
        ${categoria}
      </label>
    </li>
  `).join('');

  categoryContainer.innerHTML = checkboxesHTML;

  // Crear dropdown para móvil
  createMobileDropdown();
}

function createMobileDropdown() {
  const filterSection = document.querySelector('.section-filter');
  if (!filterSection) return;

  if (document.querySelector('.category-dropdown')) return;

  const dropdownHTML = `
    <div class="category-dropdown">
      <button type="button" class="category-dropdown-toggle">
        <span class="dropdown-text">Categorías</span>
        <span class="dropdown-arrow">▼</span>
      </button>
      <div class="category-dropdown-menu">
        <button type="button" class="category-dropdown-item active" data-category="">
          Categorías
        </button>
        ${CATEGORIAS_PRODUCTOS.map(categoria => `
          <button type="button" class="category-dropdown-item" data-category="${categoria}">
            ${categoria}
          </button>
        `).join('')}
      </div>
    </div>
  `;

  const categoryList = document.querySelector('.category-option');
  categoryList?.insertAdjacentHTML('beforebegin', dropdownHTML);

  setupDropdownEvents();
}

function setupDropdownEvents() {
  const toggle = document.querySelector('.category-dropdown-toggle');
  const menu = document.querySelector('.category-dropdown-menu');
  const items = document.querySelectorAll('.category-dropdown-item');
  const dropdownText = toggle?.querySelector('.dropdown-text');

  toggle?.addEventListener('click', () => {
    menu?.classList.toggle('show');
  });

  document.addEventListener('click', (e) => {
    if (!e.target.closest('.category-dropdown')) {
      menu?.classList.remove('show');
    }
  });

  items?.forEach(item => {
    item.addEventListener('click', () => {
      const category = item.dataset.category;

      items.forEach(i => i.classList.remove('active'));
      item.classList.add('active');
      dropdownText.textContent = item.textContent.trim();

      menu?.classList.remove('show');

      // Sincronizar checkboxes y aplicar filtro
      syncCheckboxes(category);
    });
  });
}

function syncCheckboxes(selectedCategory) {
  const checkboxes = document.querySelectorAll('input[name="category"]');
  
  checkboxes.forEach(checkbox => {
    checkbox.checked = (selectedCategory === '' ? false : checkbox.value === selectedCategory);
  });

  // Disparar evento para que filter-events.js detecte el cambio
  checkboxes[0]?.dispatchEvent(new Event('change', { bubbles: true }));
}