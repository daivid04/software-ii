import { generateModalHTML } from './modal-template.js';
import { setupModalEvents } from "./modal-event.js"; 
import { setupFilterEvents } from '../filter-product/filter-events.js';
import { renderProducts } from '../product-list/product-list.js';

/**
 * Módulo de manejo del modal para agregar/editar/ver productos.
 * Contiene funciones para abrir, cerrar y vincular el botón "Agregar producto".
 */

/**
 * Abre el modal de producto y renderiza su HTML según el tipo.
 *
 * @param {string} [type='add'] - Modo del modal: 'add' | 'edit' | 'view'.
 * @param {number|null} [id=null] - ID del producto para editar/ver; null para agregar.
 * @returns {Promise<void>} - Resuelve cuando el HTML del modal fue insertado y se inicializan eventos.
 */
export async function openModalForm(type = 'add', id = null) {
  const modalContainer = document.getElementById('modal-container');
  if(!modalContainer) return;
  
  modalContainer.innerHTML = await generateModalHTML(type, id);
  document.body.style.overflow = 'hidden';
  setupModalEvents(type,id);
}

/**
 * Cierra el modal de producto y limpia su contenido.
 * Restaura el scroll del body.
 */
export function closeModalForm() {
  const modalContainer = document.getElementById('modal-container');
  if (modalContainer) modalContainer.innerHTML = "";
  document.body.style.overflow = "";
}

/**
 * Vincula el botón con id "open-modal-btn" para abrir el modal en modo 'add'.
 * Si el botón no existe, se registra una advertencia en consola.
 *
 * Nota: el selector usa el id del elemento contenedor (li) tal como está en tus vistas.
 */
export function bindAddProductButton() {
  const addButton = document.getElementById('open-modal-btn');
  
  if (!addButton) {
    return;
  }

  addButton.addEventListener('click', (e) => {
    e.preventDefault();
    openModalForm('add');
  });
}