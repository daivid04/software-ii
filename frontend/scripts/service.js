/**
 * Módulo principal de gestión de servicios.
 * 
 * Maneja la carga de componentes UI, renderizado de servicios,
 * modales de agregar/editar y búsqueda en tiempo real.
 */

import { loadComponent } from "./utils/component-loader.js";
import { showSuccess, showError, showWarning } from "./utils/notification.js";
import { resetBodyDefaults } from "./utils/state-manager.js";
import { fetchFromApi, createResource, updateResource, deleteResource } from "./data-manager.js";
import { escapeHtml } from "./utils/sanitize.js";
import ModalFactory from "./utils/modal-factory.js";
import { truncate } from "./utils/string-helpers.js";
import { autoResizeTextarea } from "./utils/dom-helpers.js";

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

// ========== MODALES - USANDO MODALFACTORY ==========
// ModalFactory consolidates 150+ lines of duplicate modal boilerplate
// into reusable, configurable modal creation methods (form, confirm, alert)
function openAddServiceModal() {
  ModalFactory.createFormModal({
    title: 'Agregar servicio',
    submitText: 'Agregar',
    modalId: 'service-add-modal',
    fields: [
      {
        id: 'service-name',
        name: 'nombre',
        label: 'Nombre: (Máx. 100 caracteres)',
        type: 'text',
        placeholder: 'Nombre del servicio',
        required: true
      },
      {
        id: 'service-description',
        name: 'descripcion',
        label: 'Descripción: (Máx. 500 caracteres)',
        type: 'textarea',
        placeholder: 'Descripción detallada del servicio...',
        required: true
      }
    ],
    onSubmit: handleAddService
  });
}

function openEditServiceModal(serviceId) {
  const service = services.find(s => s.id === serviceId);
  if (!service) return;

  ModalFactory.createFormModal({
    title: 'Editar servicio',
    submitText: 'Modificar',
    modalId: 'service-edit-modal',
    fields: [
      {
        id: 'service-name',
        name: 'nombre',
        label: 'Nombre: (Máx. 100 caracteres)',
        type: 'text',
        placeholder: 'Nombre del servicio',
        value: service.nombre,
        required: true
      },
      {
        id: 'service-description',
        name: 'descripcion',
        label: 'Descripción: (Máx. 500 caracteres)',
        type: 'textarea',
        placeholder: 'Descripción detallada del servicio...',
        value: service.descripcion,
        required: true
      }
    ],
    onSubmit: (data) => handleEditService(data, serviceId)
  });
}

function openDeleteConfirmModal(serviceId) {
  const service = services.find(s => s.id === serviceId);
  if (!service) return;

  ModalFactory.createConfirmModal({
    title: '¿Estás seguro?',
    message: `¿Eliminar el servicio "${truncate(service.nombre, 50)}"?`,
    confirmText: 'Sí, eliminar',
    confirmClass: 'danger',
    modalId: 'service-delete-modal',
    onConfirm: () => handleDeleteService(serviceId)
  });
}

function closeModal() {
  const modal = document.querySelector('.modal');
  if (modal) {
    modal.classList.remove('show');
    setTimeout(() => modal.remove(), 300);
  }
}

// ========== MANEJADORES DE EVENTOS ==========
async function handleAddService(serviceData) {
  try {
    await createResource('servicios', serviceData);
    showSuccess('Servicio creado exitosamente');
    closeModal();
    await loadAndRenderServices();
  } catch (error) {
    showError(error.message || 'Error al crear servicio');
  }
}

async function handleEditService(serviceData, serviceId) {
  try {
    await updateResource('servicios', serviceId, serviceData);
    showSuccess('Servicio actualizado exitosamente');
    closeModal();
    await loadAndRenderServices();
  } catch (error) {
    showError(error.message || 'Error al actualizar servicio');
  }
}

async function handleDeleteService(serviceId) {
  try {
    await deleteResource('servicios', serviceId);
    showSuccess('Servicio eliminado exitosamente');
    services = [];
    filteredServices = [];
    await loadAndRenderServices();
  } catch (error) {
    showError(error.message || 'Error al eliminar servicio');
  }
}

// ========== ADJUNTAR EVENTOS A LA LISTA - EVENT DELEGATION ==========
function attachServiceEvents() {
  const serviceList = document.querySelector('.service-list');
  if (!serviceList) return;

  // Remover listeners anteriores si existen
  serviceList.removeEventListener('click', handleServiceListClick);
  
  // Agregar un único listener al contenedor
  serviceList.addEventListener('click', handleServiceListClick);
}

function handleServiceListClick(e) {
  const btnEdit = e.target.closest('.btn-edit');
  const btnDelete = e.target.closest('.btn-delete');

  if (btnEdit) {
    const serviceId = parseInt(btnEdit.dataset.id);
    openEditServiceModal(serviceId);
  } else if (btnDelete) {
    const serviceId = parseInt(btnDelete.dataset.id);
    openDeleteConfirmModal(serviceId);
  }
}

// ========== CARGAR Y RENDERIZAR ==========
async function loadAndRenderServices() {
  try {
    services = await fetchFromApi('servicios');
    filteredServices = [...services];
    renderServices();
  } catch (error) {
    showError('Error al cargar los servicios');
    services = [];
    filteredServices = [];
    renderServices();
  }
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
