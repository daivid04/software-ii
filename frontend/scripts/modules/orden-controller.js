import { setupSidebarToggle, showOrdenSidebar } from '../shared/sidebar-manager.js';
import { loadVentaProducto } from './interfaces/venta-producto.js';
import { loadServicios } from './interfaces/servicios.js';
import { loadHistorialServicios } from './interfaces/historial-servicios.js';
import { loadPendiente } from './interfaces/pendiente.js';
import { loadRevisado } from './interfaces/revisado.js';

/**
 * Controlador principal de orden
 * Orquesta las diferentes interfaces y el navegación
 */
export class OrdenController {
  constructor() {
    this.ordenContent = document.getElementById('orden-content');
    this.ordenSidebar = document.getElementById('orden-sidebar');
  }

  /**
   * Cargar sección según tipo
   */
  async loadSection(section) {
    switch (section) {
      case 'venta-producto':
        await loadVentaProducto(this.ordenContent);
        break;
      case 'servicios':
        await loadServicios(this.ordenContent);
        break;
      case 'historial-servicios':
        await loadHistorialServicios(this.ordenContent);
        break;
      case 'pendiente':
        await loadPendiente(this.ordenContent);
        break;
      case 'revisado':
        await loadRevisado(this.ordenContent);
        break;
      default:
        this.ordenContent.innerHTML = '<p>Selecciona una opción del menú</p>';
    }
  }

  /**
   * Configurar eventos del sidebar
   */
  setupSidebar() {
    const menuItems = document.querySelectorAll('.orden-sidebar-menu a');

    menuItems.forEach(item => {
      item.addEventListener('click', (e) => {
        e.preventDefault();

        // Remover clase active de todos
        menuItems.forEach(link => link.classList.remove('active'));

        // Agregar clase active al clickeado
        item.classList.add('active');

        // Cargar sección
        const section = item.dataset.section;
        this.loadSection(section);
      });
    });
  }

  /**
   * Inicializar controlador
   */
  init() {
    this.setupSidebar();
    setupSidebarToggle();
    showOrdenSidebar();
    
    // Cargar venta por defecto
    this.loadSection('venta-producto');
  }
}
