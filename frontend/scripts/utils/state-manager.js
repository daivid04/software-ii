/**
 * State Manager - Gestiona el estado global del body
 * Previene conflictos de clases CSS cuando se navega entre módulos
 */

/**
 * Limpia todas las clases de estado del body
 * Se debe llamar al inicio de cada módulo
 */
export function cleanBodyState() {
  // Clases que deben ser removidas
  const classesToRemove = [
    'inventory-open',
    'menu-open',
    'orden-open',
    'service-open',
    'sidebar-open'
  ];

  classesToRemove.forEach(className => {
    document.body.classList.remove(className);
  });

  // Resetear estilos inline que puedan estar interfiriendo
  document.body.style.overflow = '';
  document.body.style.height = '';
  document.body.style.backgroundColor = '';

  // Resetear el container también
  const container = document.querySelector('.container');
  if (container) {
    container.classList.remove('active');
    container.style.overflow = '';
    container.style.height = '';
    container.style.padding = '';
  }
}

/**
 * Resetea el estado a valores por defecto
 * Para móvil, el body debe tener overflow-y hidden
 */
export function resetBodyDefaults() {
  cleanBodyState();
  
  // Configuración inicial por defecto
  if (window.innerWidth <= 768) {
    document.body.style.overflow = 'hidden';
  }
}
