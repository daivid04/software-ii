// Cargar componentes dinámicamente
import { loadComponent } from './utils/component-loader.js';
import { resetBodyDefaults } from './utils/state-manager.js';
import { OrdenController } from './modules/orden-controller.js';

// Cargar header y sidebar dinámicamente
loadComponent("header", "includes/header.html");
loadComponent("side-bar-container", "includes/sidebar.html");

// Inicializar
document.addEventListener('DOMContentLoaded', () => {
  resetBodyDefaults();
  
  const controller = new OrdenController();
  controller.init();
});

export { OrdenController };
