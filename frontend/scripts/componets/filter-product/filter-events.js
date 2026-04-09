import { updateFilterState } from "./filtro-state.js";
import { applyFilters } from "./filter-handler.js";

export function setupFilterEvents() {
  setupCategoryFilters();
  setupStockFilter();
  setupPriceFilters();
  setupSearchFilter();
  setupClearFilters();
}

function setupCategoryFilters() {
  const categoryCheckboxes = document.querySelectorAll('input[name="category"]');
  
  categoryCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
      const selectedCategories = Array.from(
        document.querySelectorAll('input[name="category"]:checked')
      ).map(cb => cb.value);
      
      updateFilterState('selectedCategories', selectedCategories);
      applyFilters();
    });
  });
}




function setupSearchFilter(){
  const searchInput = document.querySelector('[data-search-input]');
  
  searchInput?.addEventListener('input', (e) => {
    updateFilterState('searchQuery', e.target.value.trim());
    applyFilters();
  });
}


function setupStockFilter() {
  const stockCheckbox = document.querySelector('[data-low-stock]');
  
  stockCheckbox?.addEventListener('change', (e) => {
    updateFilterState('lowStock', e.target.checked);
    applyFilters();
  });
}

function setupPriceFilters() {
  const minPriceInput = document.querySelector('[data-min-price]');
  const maxPriceInput = document.querySelector('[data-max-price]');
  
  const handlePriceChange = () => {
    const min = parseFloat(minPriceInput?.value) || null;
    const max = parseFloat(maxPriceInput?.value) || null;
    
    updateFilterState('priceRange', { min, max });
    applyFilters();
  };
  
  minPriceInput?.addEventListener('input', handlePriceChange);
  maxPriceInput?.addEventListener('input', handlePriceChange);
}

function setupClearFilters() {
  const clearButton = document.querySelector('[data-clear-filters]');
  
  clearButton?.addEventListener('click', () => {
    document.querySelectorAll('input[name="category"]').forEach(cb => cb.checked = false);
    
    const stockCheckbox = document.querySelector('[data-low-stock]');
    if (stockCheckbox) stockCheckbox.checked = false;
    
    const minPrice = document.querySelector('[data-min-price]');
    const maxPrice = document.querySelector('[data-max-price]');
    if (minPrice) minPrice.value = '';
    if (maxPrice) maxPrice.value = '';
    
    const searchInput = document.querySelector('[data-search-input]');
    if (searchInput) searchInput.value = '';
    
    // Limpiar dropdown móvil
    const dropdownItems = document.querySelectorAll('.category-dropdown-item');
    dropdownItems.forEach(item => item.classList.remove('active'));
    const firstItem = document.querySelector('.category-dropdown-item[data-category=""]');
    firstItem?.classList.add('active');
    const dropdownText = document.querySelector('.dropdown-text');
    if (dropdownText) dropdownText.textContent = 'Categorías';
    
    updateFilterState('selectedCategories', []);
    updateFilterState('lowStock', false);
    updateFilterState('priceRange', { min: null, max: null });
    updateFilterState('searchQuery', '');
    
    applyFilters();
  });
}