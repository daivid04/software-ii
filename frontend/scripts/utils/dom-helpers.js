/**
 * DOM Helpers - Utilidades reutilizables para manipulación del DOM
 * Reduce código repetitivo y estandariza operaciones comunes
 */

/**
 * Obtiene un elemento del DOM de forma segura
 * @param {string} selector - Selector CSS
 * @param {Element} parent - Elemento padre (default: document)
 * @returns {Element|null} Elemento encontrado o null
 */
export function getElement(selector, parent = document) {
  return parent.querySelector(selector);
}

/**
 * Obtiene múltiples elementos del DOM
 * @param {string} selector - Selector CSS
 * @param {Element} parent - Elemento padre (default: document)
 * @returns {NodeList} Lista de elementos
 */
export function getElements(selector, parent = document) {
  return parent.querySelectorAll(selector);
}

/**
 * Añade una clase CSS a un elemento
 * @param {Element} element - Elemento
 * @param {string} className - Nombre de la clase
 */
export function addClass(element, className) {
  if (element) element.classList.add(className);
}

/**
 * Elimina una clase CSS de un elemento
 * @param {Element} element - Elemento
 * @param {string} className - Nombre de la clase
 */
export function removeClass(element, className) {
  if (element) element.classList.remove(className);
}

/**
 * Alterna una clase CSS
 * @param {Element} element - Elemento
 * @param {string} className - Nombre de la clase
 */
export function toggleClass(element, className) {
  if (element) element.classList.toggle(className);
}

/**
 * Comprueba si un elemento tiene una clase
 * @param {Element} element - Elemento
 * @param {string} className - Nombre de la clase
 * @returns {boolean}
 */
export function hasClass(element, className) {
  return element ? element.classList.contains(className) : false;
}

/**
 * Auto-redimensiona un textarea para ajustarse al contenido
 * @param {HTMLTextAreaElement} textarea - Elemento textarea
 */
export function autoResizeTextarea(textarea) {
  if (!textarea) return;

  const resize = () => {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 400) + 'px';
  };

  textarea.addEventListener('input', resize);

  // Resize inicial
  resize();
}

/**
 * Establece múltiples atributos a un elemento
 * @param {Element} element - Elemento
 * @param {Object} attributes - Objeto con atributos a establecer
 */
export function setAttributes(element, attributes) {
  if (!element) return;
  Object.keys(attributes).forEach((key) => {
    element.setAttribute(key, attributes[key]);
  });
}

/**
 * Obtiene múltiples atributos de un elemento
 * @param {Element} element - Elemento
 * @param {Array<string>} attributeNames - Nombres de atributos
 * @returns {Object} Objeto con los atributos
 */
export function getAttributes(element, attributeNames) {
  if (!element) return {};
  const result = {};
  attributeNames.forEach((name) => {
    result[name] = element.getAttribute(name);
  });
  return result;
}

/**
 * Crea un elemento del DOM con atributos
 * @param {string} tag - Nombre de la etiqueta
 * @param {Object} attributes - Atributos del elemento
 * @param {string} content - Contenido HTML (opcional)
 * @returns {Element} Elemento creado
 */
export function createElement(tag, attributes = {}, content = '') {
  const element = document.createElement(tag);
  setAttributes(element, attributes);
  if (content) element.innerHTML = content;
  return element;
}

/**
 * Vacía un elemento de contenido
 * @param {Element} element - Elemento a vaciar
 */
export function empty(element) {
  if (element) element.innerHTML = '';
}

/**
 * Elimina un elemento del DOM
 * @param {Element} element - Elemento a eliminar
 */
export function remove(element) {
  if (element && element.parentNode) {
    element.parentNode.removeChild(element);
  }
}

/**
 * Delega un evento en un contenedor
 * @param {Element} container - Elemento contenedor
 * @param {string} eventType - Tipo de evento (click, change, etc)
 * @param {string} selector - Selector CSS para los elementos objetivo
 * @param {Function} handler - Función manejadora del evento
 */
export function delegateEvent(container, eventType, selector, handler) {
  container.addEventListener(eventType, (e) => {
    const target = e.target.closest(selector);
    if (target) {
      handler.call(target, e);
    }
  });
}

/**
 * Espera por una condición
 * @param {Function} condition - Función que retorna boolean
 * @param {number} timeout - Tiempo máximo de espera en ms (default: 5000)
 * @returns {Promise}
 */
export function waitFor(condition, timeout = 5000) {
  return new Promise((resolve, reject) => {
    const startTime = Date.now();
    const interval = setInterval(() => {
      if (condition()) {
        clearInterval(interval);
        resolve();
      } else if (Date.now() - startTime > timeout) {
        clearInterval(interval);
        reject(new Error('Timeout waiting for condition'));
      }
    }, 100);
  });
}
