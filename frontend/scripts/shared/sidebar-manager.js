// Estado del sidebar
let sidebarVisible = true;

/**
 * Alternar visibilidad del sidebar
 */
export function toggleOrdenSidebar() {
  sidebarVisible = !sidebarVisible;

  if (sidebarVisible) {
    showOrdenSidebar();
  } else {
    hideOrdenSidebar();
  }
}

/**
 * Mostrar sidebar
 */
export function showOrdenSidebar() {
  const ordenSidebar = document.getElementById('orden-sidebar');
  const mainContent = document.querySelector('.main-content');
  
  if (ordenSidebar) ordenSidebar.classList.remove('hidden');
  if (mainContent) mainContent.classList.add('with-orden-sidebar');
  
  sidebarVisible = true;
}

/**
 * Ocultar sidebar
 */
export function hideOrdenSidebar() {
  const ordenSidebar = document.getElementById('orden-sidebar');
  const mainContent = document.querySelector('.main-content');
  
  if (ordenSidebar) ordenSidebar.classList.add('hidden');
  if (mainContent) mainContent.classList.remove('with-orden-sidebar');
  
  sidebarVisible = false;
}

/**
 * Configurar toggle del sidebar desde el menú principal
 */
export function setupSidebarToggle() {
  document.addEventListener('click', (e) => {
    const ordenLink = e.target.closest('a[href="orden.html"]');

    if (ordenLink && window.location.pathname.includes('orden.html')) {
      e.preventDefault();
      toggleOrdenSidebar();
    }
  });
}
