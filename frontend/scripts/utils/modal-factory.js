/**
 * Modal Factory - Patrón Factory para crear y gestionar modales reutilizables
 * Elimina duplicación de código en la creación de formularios y confirmaciones
 */

class ModalFactory {
  /**
   * Crea un modal de formulario (Add/Edit)
   * @param {Object} config - Configuración del modal
   * @param {string} config.title - Título del modal
   * @param {string} config.submitText - Texto del botón submit
   * @param {Array<Object>} config.fields - Array de campos del formulario
   * @param {Function} config.onSubmit - Callback al enviar
   * @param {string} config.modalId - ID único del modal
   * @returns {HTMLElement} Elemento del modal
   */
  static createFormModal(config) {
    const { title, submitText, fields, onSubmit, modalId } = config;

    const modal = document.createElement('div');
    modal.id = modalId;
    modal.className = 'modal';
    modal.innerHTML = `
      <div class="modal-content">
        <div class="modal-header">
          <h2>${title}</h2>
          <button type="button" class="close-btn" aria-label="Cerrar modal">&times;</button>
        </div>
        <form id="${modalId}-form" class="modal-form">
          ${fields
            .map(
              (field) => `
            <div class="form-group">
              <label for="${field.id}">${field.label}</label>
              ${
                field.type === 'textarea'
                  ? `<textarea id="${field.id}" name="${field.name}" placeholder="${field.placeholder || ''}" ${field.required ? 'required' : ''}></textarea>`
                  : `<input type="${field.type || 'text'}" id="${field.id}" name="${field.name}" placeholder="${field.placeholder || ''}" ${field.required ? 'required' : ''} />`
              }
            </div>
          `
            )
            .join('')}
          <div class="modal-actions">
            <button type="button" class="btn btn-secondary cancel-btn">Cancelar</button>
            <button type="submit" class="btn btn-primary">${submitText}</button>
          </div>
        </form>
      </div>
    `;

    document.body.appendChild(modal);

    // Event listeners
    const closeBtn = modal.querySelector('.close-btn');
    const cancelBtn = modal.querySelector('.cancel-btn');
    const form = modal.querySelector('form');

    const closeModal = () => {
      modal.classList.remove('show');
      setTimeout(() => modal.remove(), 300);
    };

    closeBtn.addEventListener('click', closeModal);
    cancelBtn.addEventListener('click', closeModal);

    // Cerrar al hacer click en overlay
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });

    // Submit
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(form);
      const data = Object.fromEntries(formData);
      await onSubmit(data);
      closeModal();
    });

    // Mostrar modal
    setTimeout(() => modal.classList.add('show'), 10);

    return modal;
  }

  /**
   * Crea un modal de confirmación
   * @param {Object} config - Configuración del modal
   * @param {string} config.title - Título
   * @param {string} config.message - Mensaje de confirmación
   * @param {string} config.confirmText - Texto del botón confirmar
   * @param {string} config.confirmClass - Clase CSS del botón (default, danger)
   * @param {Function} config.onConfirm - Callback al confirmar
   * @param {string} config.modalId - ID único del modal
   * @returns {HTMLElement} Elemento del modal
   */
  static createConfirmModal(config) {
    const { title, message, confirmText = 'Confirmar', confirmClass = 'danger', onConfirm, modalId } = config;

    const modal = document.createElement('div');
    modal.id = modalId;
    modal.className = 'modal modal-confirm';
    modal.innerHTML = `
      <div class="modal-content modal-confirm-content">
        <div class="modal-header">
          <h2>${title}</h2>
          <button type="button" class="close-btn" aria-label="Cerrar modal">&times;</button>
        </div>
        <div class="modal-body">
          <p>${message}</p>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-secondary cancel-btn">Cancelar</button>
          <button type="button" class="btn btn-${confirmClass} confirm-btn">${confirmText}</button>
        </div>
      </div>
    `;

    document.body.appendChild(modal);

    const closeBtn = modal.querySelector('.close-btn');
    const cancelBtn = modal.querySelector('.cancel-btn');
    const confirmBtn = modal.querySelector('.confirm-btn');

    const closeModal = () => {
      modal.classList.remove('show');
      setTimeout(() => modal.remove(), 300);
    };

    closeBtn.addEventListener('click', closeModal);
    cancelBtn.addEventListener('click', closeModal);

    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });

    confirmBtn.addEventListener('click', async () => {
      await onConfirm();
      closeModal();
    });

    setTimeout(() => modal.classList.add('show'), 10);

    return modal;
  }

  /**
   * Crea un modal de alerta simple
   * @param {Object} config - Configuración del modal
   * @param {string} config.title - Título
   * @param {string} config.message - Mensaje
   * @param {string} config.buttonText - Texto del botón (default: 'Aceptar')
   * @param {string} config.modalId - ID único del modal
   * @returns {HTMLElement} Elemento del modal
   */
  static createAlertModal(config) {
    const { title, message, buttonText = 'Aceptar', modalId } = config;

    const modal = document.createElement('div');
    modal.id = modalId;
    modal.className = 'modal modal-alert';
    modal.innerHTML = `
      <div class="modal-content modal-alert-content">
        <div class="modal-header">
          <h2>${title}</h2>
        </div>
        <div class="modal-body">
          <p>${message}</p>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-primary ok-btn">${buttonText}</button>
        </div>
      </div>
    `;

    document.body.appendChild(modal);

    const okBtn = modal.querySelector('.ok-btn');

    const closeModal = () => {
      modal.classList.remove('show');
      setTimeout(() => modal.remove(), 300);
    };

    okBtn.addEventListener('click', closeModal);

    setTimeout(() => modal.classList.add('show'), 10);

    return modal;
  }
}

// Exportar para uso en módulos
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ModalFactory;
}
