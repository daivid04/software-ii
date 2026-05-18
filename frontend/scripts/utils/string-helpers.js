/**
 * String Helpers - Utilidades reutilizables para manipulación de strings
 * Proporciona funciones de propósito general para texto
 */

/**
 * Trunca un string a una longitud máxima
 * @param {string} text - Texto a truncar
 * @param {number} maxLength - Longitud máxima (default: 50)
 * @param {string} suffix - Sufijo si se trunca (default: '...')
 * @returns {string} Texto truncado
 */
export function truncate(text, maxLength = 50, suffix = '...') {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength - suffix.length) + suffix;
}

/**
 * Capitaliza la primera letra de un string
 * @param {string} text - Texto a capitalizar
 * @returns {string} Texto capitalizado
 */
export function capitalize(text) {
  if (!text) return '';
  return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
}

/**
 * Convierte a mayúsculas
 * @param {string} text - Texto
 * @returns {string} Texto en mayúsculas
 */
export function toUpperCase(text) {
  return text ? text.toUpperCase() : '';
}

/**
 * Convierte a minúsculas
 * @param {string} text - Texto
 * @returns {string} Texto en minúsculas
 */
export function toLowerCase(text) {
  return text ? text.toLowerCase() : '';
}

/**
 * Convierte un string a slug (URL-friendly)
 * @param {string} text - Texto a convertir
 * @returns {string} Slug
 */
export function slug(text) {
  if (!text) return '';
  return text
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-');
}

/**
 * Elimina espacios en blanco al inicio y final
 * @param {string} text - Texto
 * @returns {string} Texto trimmed
 */
export function trim(text) {
  return text ? text.trim() : '';
}

/**
 * Comprueba si un string está vacío o solo contiene espacios
 * @param {string} text - Texto a verificar
 * @returns {boolean}
 */
export function isEmpty(text) {
  return !text || text.trim().length === 0;
}

/**
 * Repite un string N veces
 * @param {string} text - Texto a repetir
 * @param {number} count - Número de repeticiones
 * @returns {string} Texto repetido
 */
export function repeat(text, count) {
  return (text || '').repeat(Math.max(0, count));
}

/**
 * Remplaza todas las ocurrencias de un patrón
 * @param {string} text - Texto original
 * @param {string|RegExp} search - Patrón a buscar
 * @param {string} replacement - Reemplazo
 * @returns {string} Texto con reemplazos
 */
export function replaceAll(text, search, replacement) {
  if (!text) return '';
  const regex = typeof search === 'string' ? new RegExp(search, 'g') : search;
  return text.replace(regex, replacement);
}

/**
 * Invierte un string
 * @param {string} text - Texto a invertir
 * @returns {string} Texto invertido
 */
export function reverse(text) {
  return text ? text.split('').reverse().join('') : '';
}

/**
 * Cuenta ocurrencias de un patrón en un string
 * @param {string} text - Texto
 * @param {string} pattern - Patrón a buscar
 * @returns {number} Número de ocurrencias
 */
export function countOccurrences(text, pattern) {
  if (!text || !pattern) return 0;
  const regex = new RegExp(pattern, 'g');
  const matches = text.match(regex);
  return matches ? matches.length : 0;
}

/**
 * Extrae números de un string
 * @param {string} text - Texto
 * @returns {Array<string>} Array de números encontrados
 */
export function extractNumbers(text) {
  if (!text) return [];
  return text.match(/\d+/g) || [];
}

/**
 * Genera un ID único
 * @param {string} prefix - Prefijo (opcional)
 * @returns {string} ID único
 */
export function generateId(prefix = '') {
  const timestamp = Date.now().toString(36);
  const randomStr = Math.random().toString(36).substring(2, 9);
  return prefix ? `${prefix}_${timestamp}${randomStr}` : `${timestamp}${randomStr}`;
}

/**
 * Formatea un número como moneda
 * @param {number} amount - Cantidad
 * @param {string} currency - Código de moneda (default: 'USD')
 * @param {string} locale - Locale (default: 'en-US')
 * @returns {string} Cantidad formateada
 */
export function formatCurrency(amount, currency = 'USD', locale = 'en-US') {
  try {
    return new Intl.NumberFormat(locale, {
      style: 'currency',
      currency: currency,
    }).format(amount);
  } catch {
    return `${currency} ${amount}`;
  }
}

/**
 * Formatea un número como porcentaje
 * @param {number} value - Valor
 * @param {number} decimals - Decimales (default: 2)
 * @returns {string} Porcentaje formateado
 */
export function formatPercent(value, decimals = 2) {
  return `${(value * 100).toFixed(decimals)}%`;
}

/**
 * Formatea una fecha
 * @param {Date|string} date - Fecha
 * @param {string} format - Formato (default: 'DD/MM/YYYY')
 * @returns {string} Fecha formateada
 */
export function formatDate(date, format = 'DD/MM/YYYY') {
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const hours = String(d.getHours()).padStart(2, '0');
  const minutes = String(d.getMinutes()).padStart(2, '0');
  const seconds = String(d.getSeconds()).padStart(2, '0');

  const replacements = {
    YYYY: year,
    MM: month,
    DD: day,
    HH: hours,
    mm: minutes,
    ss: seconds,
  };

  return format.replace(/YYYY|MM|DD|HH|mm|ss/g, (match) => replacements[match]);
}
