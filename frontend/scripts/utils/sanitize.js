/**
 * Utilidad para sanitizar datos y prevenir XSS (Cross-Site Scripting)
 * Escapea caracteres HTML peligrosos que podrían ejecutar scripts
 */

/**
 * Escapa caracteres HTML para prevenir XSS
 * @param {*} value - Valor a escapar
 * @returns {string} - Valor escapado y seguro para usar en HTML
 */
export function escapeHtml(value) {
  if (value === null || value === undefined) {
    return '';
  }

  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
    .replace(/\//g, '&#x2F;');
}

/**
 * Sanitiza un objeto completo, escapando todos sus valores string
 * @param {Object} obj - Objeto a sanitizar
 * @returns {Object} - Objeto con valores escapados
 */
export function sanitizeObject(obj) {
  if (!obj || typeof obj !== 'object') {
    return obj;
  }

  const sanitized = {};
  for (const [key, value] of Object.entries(obj)) {
    if (typeof value === 'string') {
      sanitized[key] = escapeHtml(value);
    } else if (typeof value === 'object' && value !== null) {
      sanitized[key] = sanitizeObject(value);
    } else {
      sanitized[key] = value;
    }
  }
  return sanitized;
}

/**
 * Crea un elemento de texto seguro (no puede contener HTML)
 * @param {string} text - Texto a mostrar
 * @returns {Text} - Nodo de texto
 */
export function createTextNode(text) {
  return document.createTextNode(String(text || ''));
}

/**
 * Establece texto de forma segura en un elemento (alternativa a innerHTML)
 * @param {HTMLElement} element - Elemento DOM
 * @param {string} text - Texto a establecer
 */
export function setTextContent(element, text) {
  if (element) {
    element.textContent = String(text || '');
  }
}

/**
 * Valida y limpia una URL para prevenir javascript: o data: URLs
 * @param {string} url - URL a validar
 * @returns {string} - URL segura o string vacío
 */
export function sanitizeUrl(url) {
  if (!url) return '';
  
  const urlStr = String(url).trim().toLowerCase();
  
  // Bloquear protocolos peligrosos
  if (urlStr.startsWith('javascript:') || 
      urlStr.startsWith('data:') || 
      urlStr.startsWith('vbscript:')) {
    return '';
  }
  
  return url;
}
