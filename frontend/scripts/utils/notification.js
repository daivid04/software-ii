import { escapeHtml } from './sanitize.js';

/**
 * Muestra una notificación flotante en pantalla.
 * @param {string} message - Texto del mensaje.
 * @param {"info"|"success"|"warning"|"error"} [type="info"] - Tipo de notificación.
 * @param {number} [duration=3000] - Duración en milisegundos.
 */
export function showNotification(message, type = "info", duration = 3000) {
  const idContainer = "notification-container";
  let container = document.getElementById(idContainer);

  if (!container) {
    container = document.createElement("div");
    container.id = idContainer;
    document.body.appendChild(container);
  }

  const noti = document.createElement("div");
  noti.className = `notification ${type}`;
  // Usar textContent en lugar de innerHTML para prevenir XSS
  const p = document.createElement('p');
  p.textContent = message;
  noti.appendChild(p);
  container.appendChild(noti);

  setTimeout(() => {
    noti.classList.add("hiding");
    setTimeout(() => {
      noti.remove();
      if (container.children.length === 0) container.remove();
    }, 300); 
}, duration);
}

export function showError(message) {
  showNotification(message, "error");
}


export function showWarning(message) {
  showNotification(message, "warning");
}


export function showSuccess(message) {
  showNotification(message, "success");
}