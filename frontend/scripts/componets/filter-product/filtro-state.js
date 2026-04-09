export const filterState = {
  searchQuery : '',
  selectedCategories: [],
  lowStock : false,
  priceRange : {
    min: null,
    max : null
  }
}

export function updateFilterState (filterName, data) {
  filterState[filterName] = data;
}

export function clearFilters () {
  filterState.searchQuery = '';
  filterState.selectedCategories = [];
  filterState.lowStock = false;
  filterState.priceRange.min = null;
  filterState.priceRange.max = null;

}