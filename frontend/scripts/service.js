/**
 * Módulo principal de gestión de servicios.
 * 
 * Maneja la carga de componentes UI, renderizado de servicios,
 * modales de agregar/editar y búsqueda en tiempo real.
 */

import { loadComponent } from "./utils/component-loader.js";
import { showSuccess, showError, showWarning } from "./utils/notification.js";
import { resetBodyDefaults } from "./utils/state-manager.js";
import { deleteResource } from "./data-manager.js";
import { escapeHtml } from "./utils/sanitize.js";

const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:8000/api/v1'  // Desarrollo local
  : '/api/v1';

// ========== CARGAR COMPONENTES UI ==========
loadComponent("header", "includes/header.html");
loadComponent("side-bar-container", "includes/sidebar.html");
loadComponent("mobile-menu-container", "includes/mobile-menu-service.html");

// ========== LIMPIAR ESTADO PREVIO ==========
// Ejecutar apenas se cargue el script
resetBodyDefaults();

// ========== ESTADO GLOBAL ==========
let services = [];
let filteredServices = [];

// ========== API: OBTENER SERVICIOS ==========
async function getServices() {
  try {
    const response = await fetch(`${API_BASE_URL}/servicios/`, {
      method: 'GET',
      headers: {
        'cache-control': 'no-cache , no-store , must-revalidate',
        'pragama': 'no-cache',
        'expires': '0',
        'Authorization': localStorage.getItem('supabase_token') ? `Bearer ${localStorage.getItem('supabase_token')}` : ''
      }
    });
    if (!response.ok) throw new Error('Error al obtener servicios');
    services = await response.json();
    filteredServices = [...services];
    return services;
  } catch (error) {
    showError('Error al cargar los servicios');
    return [];
  }
}

// ========== API: CREAR SERVICIO ==========
async function createService(serviceData) {
  try {
    const response = await fetch(`${API_BASE_URL}/servicios/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': localStorage.getItem('supabase_token') ? `Bearer ${localStorage.getItem('supabase_token')}` : ''
      },
      body: JSON.stringify(serviceData)
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Error al crear servicio');
    }

    const newService = await response.json();
    showSuccess('Servicio creado exitosamente');
    return newService;
  } catch (error) {
    showError(error.message);
    throw error;
  }
}

// ========== API: ACTUALIZAR SERVICIO ==========
async function updateService(id, serviceData) {
  try {
    const response = await fetch(`${API_BASE_URL}/servicios/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': localStorage.getItem('supabase_token') ? `Bearer ${localStorage.getItem('supabase_token')}` : ''
      },
      body: JSON.stringify(serviceData)
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Error al actualizar servicio');
    }

    const updatedService = await response.json();
    showSuccess('Servicio actualizado exitosamente');
    return updatedService;
  } catch (error) {
    showError(error.message);
    throw error;
  }
}

// ========== API: ELIMINAR SERVICIO ==========
async function deleteService(id) {
  try {
    await deleteResource('servicios', id);
    showSuccess('Servicio eliminado exitosamente');
    return true;
  } catch (error) {
    showError(error.message);
    throw error;
  }
}

// ========== UTILIDAD: AUTO-RESIZE TEXTAREA ==========
/**
 * Ajusta automáticamente la altura de un textarea según su contenido.
 * @param {HTMLTextAreaElement} textarea - El elemento textarea a ajustar
 */
function autoResizeTextarea(textarea) {
  // Resetear altura para calcular correctamente
  textarea.style.height = 'auto';

  // Calcular nueva altura basada en scrollHeight
  const newHeight = Math.min(textarea.scrollHeight, 200); // Máximo 200px
  textarea.style.height = `${newHeight}px`;
}

// ========== RENDERIZAR SERVICIOS ==========
function renderServices(servicesToRender = filteredServices) {
  const serviceList = document.querySelector('.service-list');
  if (!serviceList) return;

  if (servicesToRender.length === 0) {
    serviceList.innerHTML = `
            <div style="text-align: center; padding: 40px; color: #666;">
                <p>No hay servicios registrados</p>
            </div>
        `;
    return;
  }

  // Función para truncar texto
  const truncate = (text, maxLength) => {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  serviceList.innerHTML = servicesToRender.map(service => `
        <div class="service-row" data-service-id="${escapeHtml(service.id)}">
            <div class="service-name" title="${escapeHtml(service.nombre)}">${escapeHtml(truncate(service.nombre, 50))}</div>
            <div class="service-description" title="${escapeHtml(service.descripcion)}">${escapeHtml(truncate(service.descripcion, 100))}</div>
            <div class="service-actions">
                <button class="btn-edit" data-id="${service.id}" title="Editar">
                    <img class="img-edit" src="../assets/icons/edit.png" alt="Editar">
                </button>
                <button class="btn-delete" data-id="${service.id}" title="Eliminar">
                    <img class="img-delete" src="../assets/icons/delete.png" alt="Eliminar">
                </button>
            </div>
        </div>
    `).join('');

  // Agregar event listeners a los botones
  attachServiceEvents();
}

// ========== BÚSQUEDA EN TIEMPO REAL ==========
function setupSearch() {
  const searchInput = document.getElementById('search-input');
  if (!searchInput) return;

  searchInput.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase().trim();

    if (searchTerm === '') {
      filteredServices = [...services];
    } else {
      filteredServices = services.filter(service =>
        service.nombre.toLowerCase().includes(searchTerm) ||
        service.descripcion.toLowerCase().includes(searchTerm)
      );
    }

    renderServices();
  });
}

// ========== MODALES ==========
function openAddServiceModal() {
  const modalContainer = document.getElementById('modal-container');
  if (!modalContainer) return;

  modalContainer.innerHTML = `
        <div class="modal-overlay" id="service-modal-overlay">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>Agregar servicio</h2>
                    <button class="modal-close" id="close-service-modal">X</button>
                </div>
                <form id="service-form" class="modal-body">
                    <div class="form-group">
                        <label for="service-name">Nombre: <small>(Máx. 100 caracteres)</small></label>
                        <input 
                            type="text" 
                            id="service-name" 
                            name="nombre" 
                            placeholder="Nombre del servicio"
                            maxlength="100"
                            required
                        />
                    </div>
                    
                    <div class="form-group">
                        <label for="service-description">Descripción: <small>(Máx. 500 caracteres)</small></label>
                        <textarea 
                            id="service-description" 
                            name="descripcion" 
                            placeholder="Descripción detallada del servicio..."
                            rows="3"
                            maxlength="500"
                            required
                        ></textarea>
                    </div>
                    <p class="form-hint">El precio del servicio se define al agregarlo a una orden.</p>
                    
                    <div class="modal-actions">
                        <button type="submit" class="btn-primary">Agregar</button>
                    </div>
                </form>
            </div>
        </div>
    `;

  // Event listeners del modal
  const closeBtn = document.getElementById('close-service-modal');
  const overlay = document.getElementById('service-modal-overlay');
  const form = document.getElementById('service-form');
  const textarea = document.getElementById('service-description');

  if (closeBtn) {
    closeBtn.addEventListener('click', closeModal);
  }

  if (overlay) {
    overlay.addEventListener('click', (e) => {
      if (e.target.id === 'service-modal-overlay') closeModal();
    });
  }

  // Auto-resize del textarea
  if (textarea) {
    autoResizeTextarea(textarea);
    textarea.addEventListener('input', () => autoResizeTextarea(textarea));
  }

  if (form) {
    form.addEventListener('submit', handleAddService);
  }
}

function openEditServiceModal(serviceId) {
  const service = services.find(s => s.id === serviceId);
  if (!service) return;

  const modalContainer = document.getElementById('modal-container');
  if (!modalContainer) return;

  modalContainer.innerHTML = `
        <div class="modal-overlay" id="service-modal-overlay">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>Editar servicio</h2>
                    <button class="modal-close" id="close-service-modal">X</button>
                </div>
                <form id="service-form" class="modal-body">
                    <div class="form-group">
                        <label for="service-name">Nombre: <small>(Máx. 100 caracteres)</small></label>
                        <input 
                            type="text" 
                            id="service-name" 
                            name="nombre" 
                            value="${service.nombre}"
                            maxlength="100"
                            required
                        />
                    </div>
                    
                    <div class="form-group">
                        <label for="service-description">Descripción: <small>(Máx. 500 caracteres)</small></label>
                        <textarea 
                            id="service-description" 
                            name="descripcion" 
                            rows="3"
                            maxlength="500"
                            required
                        >${service.descripcion}</textarea>
                    </div>
                    <p class="form-hint">El precio se asigna directamente en la orden que use este servicio.</p>
                    
                    <div class="modal-actions">
                        <button type="submit" class="btn-primary">Modificar</button>
                    </div>
                </form>
            </div>
        </div>
    `;

  // Event listeners del modal
  const closeBtn = document.getElementById('close-service-modal');
  const overlay = document.getElementById('service-modal-overlay');
  const form = document.getElementById('service-form');
  const textarea = document.getElementById('service-description');

  if (closeBtn) {
    closeBtn.addEventListener('click', closeModal);
  }

  if (overlay) {
    overlay.addEventListener('click', (e) => {
      if (e.target.id === 'service-modal-overlay') closeModal();
    });
  }

  // Auto-resize del textarea
  if (textarea) {
    autoResizeTextarea(textarea);
    textarea.addEventListener('input', () => autoResizeTextarea(textarea));
  }

  if (form) {
    form.addEventListener('submit', (e) => {
      handleEditService(e, serviceId);
    });
  }
}

function openDeleteConfirmModal(serviceId) {
  const service = services.find(s => s.id === serviceId);
  if (!service) return;

  const modalContainer = document.getElementById('modal-container');
  if (!modalContainer) return;

  // Truncar nombre si es muy largo
  const truncatedName = service.nombre.length > 50
    ? service.nombre.substring(0, 50) + '...'
    : service.nombre;

  modalContainer.innerHTML = `
        <div class="modal-overlay" id="confirm-modal-overlay">
            <div class="modal-confirm">
                <div class="modal-icon">⚠️</div>
                <h3>¿Estas seguro de eliminar el servicio <strong>${truncatedName}</strong>?</h3>
                <div class="modal-confirm-actions">
                    <button class="btn-confirm-yes" id="confirm-delete">Sí</button>
                    <button class="btn-confirm-no" id="cancel-delete">No</button>
                </div>
            </div>
        </div>
    `;

  document.getElementById('confirm-delete').addEventListener('click', async () => {
    await handleDeleteService(serviceId);
    closeModal();
  });

  document.getElementById('cancel-delete').addEventListener('click', closeModal);
  document.getElementById('confirm-modal-overlay').addEventListener('click', (e) => {
    if (e.target.id === 'confirm-modal-overlay') closeModal();
  });
}

function closeModal() {
  const modalContainer = document.getElementById('modal-container');
  if (modalContainer) modalContainer.innerHTML = '';
}

// ========== MANEJADORES DE EVENTOS ==========
async function handleAddService(e) {
  e.preventDefault();

  const formData = new FormData(e.target);
  const serviceData = {
    nombre: formData.get('nombre'),
    descripcion: formData.get('descripcion')
  };

  try {
    await createService(serviceData);
    closeModal();
    await loadAndRenderServices();
  } catch (error) {
    // El error ya se muestra en createService
  }
}

async function handleEditService(e, serviceId) {
  e.preventDefault();

  const formData = new FormData(e.target);
  const serviceData = {
    nombre: formData.get('nombre'),
    descripcion: formData.get('descripcion')
  };

  try {
    await updateService(serviceId, serviceData);
    closeModal();
    await loadAndRenderServices();
  } catch (error) {
    // El error ya se muestra en updateService
  }
}

async function handleDeleteService(serviceId) {
  try {
    await deleteService(serviceId);
    // Forzar recarga de datos frescos desde el servidor
    services = []; // Limpiar array local
    filteredServices = []; // Limpiar array filtrado
    await loadAndRenderServices(); // Recargar y renderizar
  } catch (error) {
    // El error ya se muestra en deleteService
  }
}

// ========== ADJUNTAR EVENTOS A LA LISTA ==========
function attachServiceEvents() {
  // Botones de editar
  document.querySelectorAll('.btn-edit').forEach(btn => {
    btn.addEventListener('click', () => {
      const serviceId = parseInt(btn.dataset.id);
      openEditServiceModal(serviceId);
    });
  });

  // Botones de eliminar
  document.querySelectorAll('.btn-delete').forEach(btn => {
    btn.addEventListener('click', () => {
      const serviceId = parseInt(btn.dataset.id);
      openDeleteConfirmModal(serviceId);
    });
  });
}

// ========== CARGAR Y RENDERIZAR ==========
async function loadAndRenderServices() {
  await getServices();
  renderServices();
}

// ========== CONTROLADOR MENÚ MÓVIL ==========
function setupMobileMenuControler() {
  const btnList = document.getElementById("service-mobile-btn-list");
  const btnAdd = document.getElementById("service-mobile-btn-add");
  const btnBack = document.getElementById("mobile-back-btn");

  const mainContent = document.querySelector(".main-content");
  const mobileMenu = document.querySelector("#mobile-menu-container");

  if (btnList) {
    btnList.addEventListener('click', () => {
      // Toggle: si está activo, lo oculta; si está oculto, lo muestra
      if (mainContent.classList.contains('active')) {
        // Volver al menú principal
        mainContent.classList.remove('active');
        mobileMenu.classList.remove('active');
      } else {
        // Mostrar la lista de servicios
        mainContent.classList.add('active');
        mobileMenu.classList.add('active');
      }
    });
  }

  if (btnAdd) {
    btnAdd.addEventListener('click', () => {
      openAddServiceModal();
    });
  }

  // Botón "Volver" en la vista de servicios
  if (btnBack) {
    btnBack.addEventListener('click', () => {
      mainContent.classList.remove('active');
      mobileMenu.classList.remove('active');
    });
  }
}

// ========== INICIALIZACIÓN ==========
document.addEventListener('DOMContentLoaded', async () => {
  // Cargar servicios
  await loadAndRenderServices();

  // Configurar búsqueda
  setupSearch();

  // Configurar menú móvil
  setupMobileMenuControler();

  // Botón agregar servicio
  const openModalBtn = document.getElementById('open-modal-btn');
  if (openModalBtn) {
    openModalBtn.addEventListener('click', (e) => {
      e.preventDefault();
      openAddServiceModal();
    });
  }
});
