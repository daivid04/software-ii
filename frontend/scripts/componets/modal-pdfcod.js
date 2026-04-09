/**
 * ========================================
 * MODAL PARA DESCARGA DE CÓDIGOS DE BARRAS EN PDF
 * ========================================
 * 
 * Este módulo maneja la apertura del modal, selección de opciones
 * de fecha y generación del PDF con códigos de barras.
 */

import { countFromApi, fetchFromApi } from "../data-manager.js";
import { showNotification } from "../utils/notification.js";

// ========================================
// CONSTANTES Y CONFIGURACIÓN
// ========================================

/**
 * Opciones de rango de fechas para filtrar productos
 * Cada opción define días hacia atrás desde la fecha actual
 */
const DATE_OPTIONS = [
    { id: 'last-day', label: 'Último día', days: 1 },
    { id: 'last-3-days', label: 'Últimos 3 días', days: 3 },
    { id: 'last-week', label: 'Última semana', days: 7 },
    { id: 'last-15-days', label: 'Últimos 15 días', days: 15 },
    { id: 'last-month', label: 'Último mes', days: 30 },
    { id: 'all', label: 'Todos los productos', days: null }
];

/**
 * Opciones de tamaño de página para el PDF
 */
const PAGE_SIZE_OPTIONS = [
    { id: 'a4', label: 'A4 (Estándar)', value: 'a4' },
    { id: 'letter', label: 'Carta (Letter)', value: 'letter' },
    { id: 'a5', label: 'A5 (Pequeño)', value: 'a5' }
];

/**
 * Opciones de columnas por página
 */
const COLUMN_OPTIONS = [
    { id: 'cols-2', label: '2 columnas', value: 2 },
    { id: 'cols-3', label: '3 columnas', value: 3 },
    { id: 'cols-4', label: '4 columnas (compacto)', value: 4 }
];

/**
 * Opciones de categorías para filtrar
 */
let CATEGORY_OPTIONS = [
    { id: 'cat-all', label: 'Todas las categorías', value: 'all' }
];

/**
 * Opciones de ordenamiento
 */
const SORT_OPTIONS = [
    { id: 'sort-name-asc', label: 'Nombre (A-Z)', value: 'name-asc' },
    { id: 'sort-name-desc', label: 'Nombre (Z-A)', value: 'name-desc' },
    //{ id: 'sort-date-desc', label: 'Más recientes primero', value: 'date-desc' },
    //{ id: 'sort-date-asc', label: 'Más antiguos primero', value: 'date-asc' },
    { id: 'sort-code', label: 'Por código de barras', value: 'code' }
];

// ========================================
// FUNCIONES DE TEMPLATE HTML
// ========================================

/**
 * Genera el HTML del modal para seleccionar opciones de descarga
 * @returns {string} HTML del modal
 */
function generateModalHTML() {
    // Opciones de rango de fecha
    const dateOptionsHTML = DATE_OPTIONS.map(option => `
        <label class="pdf-option-item" data-days="${option.days}">
            <input type="radio" name="date-range" value="${option.id}" ${option.id === 'last-week' ? 'checked' : ''}>
            <span class="option-radio"></span>
            <span class="option-label">${option.label}</span>
        </label>
    `).join('');

    // Opciones de categorías
    const categoryOptionsHTML = CATEGORY_OPTIONS.map(option => `
        <option value="${option.value}" ${option.value === 'all' ? 'selected' : ''}>${option.label}</option>
    `).join('');

    // Opciones de tamaño de página
    const pageSizeOptionsHTML = PAGE_SIZE_OPTIONS.map(option => `
        <option value="${option.value}" ${option.value === 'a4' ? 'selected' : ''}>${option.label}</option>
    `).join('');

    // Opciones de columnas
    const columnOptionsHTML = COLUMN_OPTIONS.map(option => `
        <option value="${option.value}" ${option.value === 2 ? 'selected' : ''}>${option.label}</option>
    `).join('');

    // Opciones de ordenamiento
    const sortOptionsHTML = SORT_OPTIONS.map(option => `
        <option value="${option.value}" ${option.value === 'name-asc' ? 'selected' : ''}>${option.label}</option>
    `).join('');

    return `
        <div class="modal-overlay" id="modal-pdf-overlay">
            <div class="modal-content modal-pdf-content">
                <!-- Encabezado del modal -->
                <div class="modal-header">
                    <h2>
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
                            <line x1="3" y1="6" x2="21" y2="6"></line>
                            <path d="M16 10a4 4 0 0 1-8 0"></path>
                        </svg>
                        Descargar Códigos de Barras
                    </h2>
                    <button class="modal-close-btn" id="close-pdf-modal" aria-label="Cerrar">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <line x1="18" y1="6" x2="6" y2="18"></line>
                            <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                    </button>
                </div>

                <!-- Cuerpo del modal -->
                <div class="modal-body">
                    <p class="modal-description">
                        Configura las opciones para generar el PDF con los códigos de barras.
                    </p>

                    <!-- Sección: Rango de tiempo -->
                    <!-- <div class="pdf-options-container">
                        <h4>
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <circle cx="12" cy="12" r="10"></circle>
                                <polyline points="12 6 12 12 16 14"></polyline>
                            </svg>
                            Rango de tiempo
                        </h4>
                        <div class="pdf-options-list">
                            ${dateOptionsHTML}
                        </div>
                    </div>
                    -->
                    <!-- Sección: Filtros adicionales -->
                    <div class="pdf-options-container pdf-filters-section">
                        <h4>
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
                            </svg>
                            Filtros
                        </h4>
                        <div class="pdf-filter-row">
                            <div class="pdf-filter-group">
                                <label for="category-filter">Categoría</label>
                                <select id="category-filter" class="pdf-select">
                                    ${categoryOptionsHTML}
                                </select>
                            </div>
                            <div class="pdf-filter-group">
                                <label for="sort-filter">Ordenar por</label>
                                <select id="sort-filter" class="pdf-select">
                                    ${sortOptionsHTML}
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- Sección: Configuración del PDF -->
                    <div class="pdf-options-container pdf-config-section">
                        <h4>
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                                <polyline points="14 2 14 8 20 8"></polyline>
                            </svg>
                            Configuración del PDF
                        </h4>
                        <div class="pdf-filter-row">
                            <div class="pdf-filter-group">
                                <label for="page-size">Tamaño de página</label>
                                <select id="page-size" class="pdf-select">
                                    ${pageSizeOptionsHTML}
                                </select>
                            </div>
                            <div class="pdf-filter-group">
                                <label for="columns-count">Columnas</label>
                                <select id="columns-count" class="pdf-select">
                                    ${columnOptionsHTML}
                                </select>
                            </div>
                        </div>
                        
                        <!-- Opciones adicionales con checkboxes -->
                        <div class="pdf-checkbox-options">
                            <label class="pdf-checkbox-item">
                                <input type="checkbox" id="include-product-name" checked>
                                <span class="checkbox-mark"></span>
                                <span>Incluir nombre del producto</span>
                            </label>
                            <label class="pdf-checkbox-item">
                                <input type="checkbox" id="include-price" checked>
                                <span class="checkbox-mark"></span>
                                <span>Incluir precio de venta</span>
                            </label>
                            <label class="pdf-checkbox-item">
                                <input type="checkbox" id="include-category">
                                <span class="checkbox-mark"></span>
                                <span>Incluir categoría</span>
                            </label>
                            <label class="pdf-checkbox-item">
                                <input type="checkbox" id="include-header" checked>
                                <span class="checkbox-mark"></span>
                                <span>Incluir encabezado del taller</span>
                            </label>
                        </div>
                    </div>

                    <!-- Vista previa de cantidad -->
                    <div class="pdf-preview-info" id="pdf-preview-info">
                        <div class="preview-icon">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <circle cx="12" cy="12" r="10"></circle>
                                <line x1="12" y1="16" x2="12" y2="12"></line>
                                <line x1="12" y1="8" x2="12.01" y2="8"></line>
                            </svg>
                        </div>
                        <span id="products-count-text">Calculando productos...</span>
                    </div>
                </div>

                <!-- Pie del modal -->
                <div class="modal-footer">
                    <button class="btn-cancel" id="btn-cancel-pdf">Cancelar</button>
                    <button class="btn-preview" id="btn-preview-pdf">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                            <circle cx="12" cy="12" r="3"></circle>
                        </svg>
                        Vista previa
                    </button>
                    <button class="btn-download" id="btn-download-pdf">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                            <polyline points="7 10 12 15 17 10"></polyline>
                            <line x1="12" y1="15" x2="12" y2="3"></line>
                        </svg>
                        Descargar PDF
                    </button>
                </div>
            </div>
        </div>
    `;
}

// ========================================
// FUNCIONES DE LÓGICA
// ========================================

/**
 * Obtiene la fecha límite según los días seleccionados
 * @param {number|null} days - Número de días hacia atrás (null = todos)
 * @returns {Date|null} Fecha límite o null si son todos
 */
function getDateLimit(days) {
    if (days === null) return null;

    const date = new Date();
    date.setDate(date.getDate() - days);
    date.setHours(0, 0, 0, 0);
    return date;
}

/**
 * Filtra productos por rango de fecha de creación
 * @param {Array} products - Lista de productos
 * @param {number|null} days - Días hacia atrás para filtrar
 * @returns {Array} Productos filtrados que tienen código de barras
 */
function filterProductsByDate(products, days) {
    // Filtrar solo productos con código de barras
    let filtered = products.filter(p => p.codBarras && p.codBarras.trim() !== '');

    if (days === null) {
        return filtered; // Todos los productos con código
    }

    const dateLimit = getDateLimit(days);

    return filtered.filter(product => {
        // Usar fecha de creación si existe, si no, incluir el producto
        if (!product.fechaCreacion && !product.created_at && !product.fecha_creacion) {
            return true; // Incluir productos sin fecha (por compatibilidad)
        }

        const createdDate = new Date(
            product.fechaCreacion || product.created_at || product.fecha_creacion
        );
        return createdDate >= dateLimit;
    });
}

/**
 * Filtra productos por categoría
 * @param {Array} products - Lista de productos
 * @param {string} category - Categoría seleccionada ('all' para todas)
 * @returns {Array} Productos filtrados
 */
function filterProductsByCategory(products, category) {
    if (category === 'all') return products;
    return products.filter(p => p.categoria === category || p.category === category);
}

/**
 * Ordena productos según criterio seleccionado
 * @param {Array} products - Lista de productos
 * @param {string} sortBy - Criterio de ordenamiento
 * @returns {Array} Productos ordenados
 */
function sortProducts(products, sortBy) {
    const sorted = [...products];

    switch (sortBy) {
        case 'name-asc':
            return sorted.sort((a, b) => (a.nombre || '').localeCompare(b.nombre || ''));
        case 'name-desc':
            return sorted.sort((a, b) => (b.nombre || '').localeCompare(a.nombre || ''));
        case 'date-desc':
            return sorted.sort((a, b) => {
                const dateA = new Date(a.fechaCreacion || a.created_at || 0);
                const dateB = new Date(b.fechaCreacion || b.created_at || 0);
                return dateB - dateA;
            });
        case 'date-asc':
            return sorted.sort((a, b) => {
                const dateA = new Date(a.fechaCreacion || a.created_at || 0);
                const dateB = new Date(b.fechaCreacion || b.created_at || 0);
                return dateA - dateB;
            });
        case 'code':
            return sorted.sort((a, b) => (a.codBarras || '').localeCompare(b.codBarras || ''));
        default:
            return sorted;
    }
}

/**
 * Obtiene las opciones actuales del modal
 * @returns {Object} Configuración seleccionada
 */
function getModalOptions() {
    return {
        dateRange: document.querySelector('input[name="date-range"]:checked')?.value || 'last-week',
        category: document.getElementById('category-filter')?.value || 'all',
        sortBy: document.getElementById('sort-filter')?.value || 'name-asc',
        pageSize: document.getElementById('page-size')?.value || 'a4',
        columns: parseInt(document.getElementById('columns-count')?.value) || 2,
        includeProductName: document.getElementById('include-product-name')?.checked ?? true,
        includePrice: document.getElementById('include-price')?.checked ?? true,
        includeCategory: document.getElementById('include-category')?.checked ?? false,
        includeHeader: document.getElementById('include-header')?.checked ?? true
    };
}

/**
 * Aplica todos los filtros a los productos
 * @param {Array} products - Lista de productos
 * @param {Object} options - Opciones del modal
 * @returns {Array} Productos filtrados y ordenados
 */
function applyAllFilters(products, options) {
    const dateOption = DATE_OPTIONS.find(opt => opt.id === options.dateRange);
    let filtered = filterProductsByDate(products, dateOption?.days);
    filtered = filterProductsByCategory(filtered, options.category);
    filtered = sortProducts(filtered, options.sortBy);
    return filtered;
}

/**
 * Actualiza el contador de productos en la vista previa
 * @param {Array} products - Lista de productos original
 * @param {number|null} days - Días seleccionados
 */
async function updateProductCount(products, days) {
    const countText = document.getElementById('products-count-text');
    const previewInfo = document.getElementById('pdf-preview-info');

    if (!countText) return;

    const filtered = filterProductsByDate(products, days);
    const count = filtered.length;

    if (count === 0) {
        countText.textContent = 'No hay productos con código de barras en este período';
        previewInfo?.classList.add('warning');
        previewInfo?.classList.remove('success');
    } else {
        const label = days === null ? 'en total' : `en los últimos ${days} día${days > 1 ? 's' : ''}`;
        countText.textContent = `${count} producto${count > 1 ? 's' : ''} con código de barras ${label}`;
        previewInfo?.classList.add('success');
        previewInfo?.classList.remove('warning');
    }
}

/**
 * Genera el PDF con los códigos de barras
 * @param {Array} products - Productos filtrados
 * @param {string} optionLabel - Etiqueta de la opción seleccionada (para nombre del archivo)
 * @param {Object} options - Opciones de configuración del PDF
 */
async function generatePDF(products, optionLabel, options = {}) {
    // Verificar que jsPDF esté disponible
    if (typeof window.jspdf === 'undefined') {
        // Cargar jsPDF dinámicamente si no está disponible
        await loadJsPDF();
    }

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF('p', 'mm', options.pageSize || 'a4');

    // Configuración del documento según opciones
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    const margin = 10;
    const cols = options.columns || 3;
    const gap = 2; // Espacio entre columnas
    const colWidth = (pageWidth - margin * 2 - gap * (cols - 1)) / cols;

    // Ajustar tamaño de código de barras según columnas
    const barcodeWidth = colWidth - 8;
    const barcodeHeight = cols >= 4 ? 22 : (cols === 3 ? 26 : 30);

    // Calcular altura del item - más compacto
    let itemHeight = barcodeHeight + 4; // Código + padding mínimo
    if (options.includeProductName) itemHeight += 10;
    if (options.includeCategory) itemHeight += 8;

    let currentY = margin;
    let currentCol = 0;
    let pageNumber = 1;

    // Encabezado del documento (si está habilitado)
    if (options.includeHeader) {
        // Título simple del taller
        doc.setFontSize(16);
        doc.setFont('helvetica', 'bold');
        doc.setTextColor(0, 91, 182);
        doc.text('TALLER DE DIEGO', pageWidth / 2, currentY + 5, { align: 'center' });

        currentY += 10;
        doc.setFontSize(9);
        doc.setFont('helvetica', 'normal');
        doc.setTextColor(100);
        doc.text(`${optionLabel} | ${products.length} productos | ${new Date().toLocaleDateString('es-PE')}`, pageWidth / 2, currentY, { align: 'center' });

        currentY += 6;

        // Línea separadora simple
        doc.setDrawColor(200);
        doc.setLineWidth(0.3);
        doc.line(margin, currentY, pageWidth - margin, currentY);
        currentY += 6;
    }

    doc.setTextColor(0);

    // Generar códigos de barras
    for (let i = 0; i < products.length; i++) {
        const product = products[i];

        // Calcular posición X con gap
        const x = margin + (currentCol * (colWidth + gap));

        // Verificar si necesitamos nueva página
        if (currentY + itemHeight > pageHeight - 10) {
            doc.addPage();
            pageNumber++;
            currentY = margin;
            currentCol = 0;
        }

        // Línea delimitadora simple (solo borde)
        doc.setDrawColor(180);
        doc.setLineWidth(0.2);
        doc.rect(x, currentY, colWidth, itemHeight);

        // Posición Y inicial dentro del recuadro
        let textY = currentY + 3;

        // Generar imagen del código de barras PRIMERO (arriba)
        try {
            const barcodeDataUrl = await generateBarcodeDataUrl(product.codBarras, cols);
            if (barcodeDataUrl) {
                const imgX = x + (colWidth - barcodeWidth) / 2;
                doc.addImage(barcodeDataUrl, 'PNG', imgX, textY, barcodeWidth, barcodeHeight);
                textY += barcodeHeight + 2;
            }
        } catch (error) {
            doc.setFontSize(7);
            doc.setTextColor(200, 0, 0);
            doc.text('Error', x + colWidth / 2, textY + 10, { align: 'center' });
            doc.setTextColor(0);
            textY += barcodeHeight + 2;
        }

        // Nombre del producto (debajo del código, centrado)
        if (options.includeProductName) {
            doc.setFontSize(cols >= 4 ? 7 : (cols === 3 ? 8 : 9));
            doc.setFont('helvetica', 'bold');
            doc.setTextColor(30, 30, 30);
            const maxChars = cols >= 4 ? 18 : (cols === 3 ? 24 : 30);
            const productName = truncateText(product.nombre || 'Sin nombre', maxChars);
            doc.text(productName, x + colWidth / 2, textY + 1, { align: 'center' });
            textY += 5;
        }

        // Categoría (si está habilitada, debajo del nombre)
        if (options.includeCategory && product.categoria) {
            doc.setFontSize(cols >= 4 ? 6 : 7);
            doc.setFont('helvetica', 'normal');
            doc.setTextColor(100);
            doc.text(`Cat: ${product.categoria}`, x + colWidth / 2, textY + 1, { align: 'center' });
        }

        // Siguiente columna o fila
        currentCol++;
        if (currentCol >= cols) {
            currentCol = 0;
            currentY += itemHeight;
        }
    }

    // Pie de página simple
    doc.setFontSize(7);
    doc.setTextColor(150);
    doc.text(`Taller de Diego | Pág. ${pageNumber}`, pageWidth / 2, pageHeight - 5, { align: 'center' });

    // Nombre del archivo simple basado en la opción seleccionada
    const fileName = `${sanitizeFileName(optionLabel)}.pdf`;

    // Descargar PDF
    doc.save(fileName);

    return fileName;
}

/**
 * Genera una imagen Data URL del código de barras
 * @param {string} barcodeValue - Valor del código de barras
 * @param {number} cols - Número de columnas (para ajustar tamaño)
 * @returns {Promise<string>} Data URL de la imagen PNG
 */
async function generateBarcodeDataUrl(barcodeValue, cols = 2) {
    return new Promise((resolve, reject) => {
        try {
            if (typeof JsBarcode === 'undefined') {
                reject(new Error('JsBarcode no está disponible'));
                return;
            }

            const canvas = document.createElement('canvas');

            // Ajustar tamaño según columnas
            const width = cols >= 4 ? 200 : (cols === 3 ? 250 : 300);
            const height = cols >= 4 ? 70 : (cols === 3 ? 80 : 100);
            const barcodeHeight = cols >= 4 ? 40 : (cols === 3 ? 50 : 60);
            const fontSize = cols >= 4 ? 10 : (cols === 3 ? 12 : 14);

            canvas.width = width;
            canvas.height = height;

            JsBarcode(canvas, barcodeValue, {
                format: 'CODE128',
                width: cols >= 4 ? 1.5 : 2,
                height: barcodeHeight,
                displayValue: true,
                fontSize: fontSize,
                fontOptions: 'bold',
                textAlign: 'center',
                textMargin: 3,
                margin: 8,
                background: '#ffffff',
                lineColor: '#000000'
            });

            resolve(canvas.toDataURL('image/png'));
        } catch (error) {
            reject(error);
        }
    });
}

/**
 * Carga la librería jsPDF dinámicamente
 */
async function loadJsPDF() {
    return new Promise((resolve, reject) => {
        if (typeof window.jspdf !== 'undefined') {
            resolve();
            return;
        }

        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js';
        script.onload = () => resolve();
        script.onerror = () => reject(new Error('No se pudo cargar jsPDF'));
        document.head.appendChild(script);
    });
}

// ========================================
// FUNCIONES AUXILIARES
// ========================================

/**
 * Trunca texto a un máximo de caracteres
 */
function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength - 3) + '...';
}

/**
 * Sanitiza texto para nombre de archivo
 */
function sanitizeFileName(text) {
    return text
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .replace(/[^a-z0-9]+/g, '_')
        .replace(/^_+|_+$/g, '');
}

/**
 * Formatea fecha para nombre de archivo
 */
function formatDateForFile(date) {
    return date.toISOString().split('T')[0].replace(/-/g, '');
}

// ========================================
// FUNCIONES DE CONTROL DEL MODAL
// ========================================

/**
 * Abre el modal de descarga de códigos de barras
 */
export async function openBarcodeModal() {
    const modalContainer = document.getElementById('modal-container');
    if (!modalContainer) {
        return;
    }

    // Cargar productos primero para obtener categorías
    let products = [];
    try {
        products = await fetchFromApi('productos');

        // Extraer categorías únicas de los productos
        const categories = [...new Set(products
            .filter(p => p.categoria)
            .map(p => p.categoria)
        )].sort();

        // Actualizar opciones de categorías
        CATEGORY_OPTIONS = [
            { id: 'cat-all', label: 'Todas las categorías', value: 'all' },
            ...categories.map(cat => ({
                id: `cat-${cat.toLowerCase().replace(/\s+/g, '-')}`,
                label: cat,
                value: cat
            }))
        ];
    } catch (error) {
        showNotification('Error al cargar productos', 'error');
    }

    // Insertar HTML del modal
    modalContainer.innerHTML = generateModalHTML();
    document.body.style.overflow = 'hidden';

    // Configurar eventos
    setupModalEvents(products);

    // Actualizar conteo inicial (última semana por defecto)
    updateProductCountWithFilters(products);
}

/**
 * Actualiza el contador de productos considerando todos los filtros
 * @param {Array} products - Lista de productos
 */
function updateProductCountWithFilters(products) {
    const options = getModalOptions();
    const filtered = applyAllFilters(products, options);
    const count = filtered.length;

    const countText = document.getElementById('products-count-text');
    const previewInfo = document.getElementById('pdf-preview-info');

    if (!countText) return;

    if (count === 0) {
        countText.textContent = 'No hay productos con código de barras con estos filtros';
        previewInfo?.classList.add('warning');
        previewInfo?.classList.remove('success');
    } else {
        const dateOption = DATE_OPTIONS.find(opt => opt.id === options.dateRange);
        const dateLabel = dateOption?.days === null ? '' : ` (${dateOption?.label.toLowerCase()})`;
        const categoryLabel = options.category !== 'all' ? ` - ${options.category}` : '';
        countText.textContent = `${count} producto${count > 1 ? 's' : ''} con código de barras seleccionado${count > 1 ? 's' : ''} `;
        previewInfo?.classList.add('success');
        previewInfo?.classList.remove('warning');
    }
}

/**
 * Cierra el modal de códigos de barras
 */
export function closeBarcodeModal() {
    const modalContainer = document.getElementById('modal-container');
    if (modalContainer) {
        modalContainer.innerHTML = '';
    }
    document.body.style.overflow = '';
}

/**
 * Configura los eventos del modal
 * @param {Array} products - Lista de productos
 */
function setupModalEvents(products) {
    // Cerrar con botón X
    const closeBtn = document.getElementById('close-pdf-modal');
    closeBtn?.addEventListener('click', closeBarcodeModal);

    // Cerrar con botón Cancelar
    const cancelBtn = document.getElementById('btn-cancel-pdf');
    cancelBtn?.addEventListener('click', closeBarcodeModal);

    // Cerrar al hacer clic fuera del modal
    const overlay = document.getElementById('modal-pdf-overlay');
    overlay?.addEventListener('click', (e) => {
        if (e.target === overlay) {
            closeBarcodeModal();
        }
    });

    // Cerrar con tecla Escape
    const handleEscape = (e) => {
        if (e.key === 'Escape') {
            closeBarcodeModal();
            document.removeEventListener('keydown', handleEscape);
        }
    };
    document.addEventListener('keydown', handleEscape);

    // Función para actualizar conteo cuando cambia cualquier filtro
    const updateCount = () => updateProductCountWithFilters(products);

    // Cambiar opción de fecha
    const radioInputs = document.querySelectorAll('input[name="date-range"]');
    radioInputs.forEach(input => {
        input.addEventListener('change', updateCount);
    });

    // Cambiar categoría
    const categoryFilter = document.getElementById('category-filter');
    categoryFilter?.addEventListener('change', updateCount);

    // Cambiar ordenamiento (no afecta conteo, pero preparado para futuro)
    const sortFilter = document.getElementById('sort-filter');
    sortFilter?.addEventListener('change', updateCount);

    // Botón de vista previa
    const previewBtn = document.getElementById('btn-preview-pdf');
    previewBtn?.addEventListener('click', async () => {
        const options = getModalOptions();
        const dateOption = DATE_OPTIONS.find(opt => opt.id === options.dateRange);
        const filtered = applyAllFilters(products, options);

        if (filtered.length === 0) {
            showNotification('No hay productos con estos filtros', 'warning');
            return;
        }

        // Mostrar estado de carga
        previewBtn.disabled = true;
        const originalContent = previewBtn.innerHTML;
        previewBtn.innerHTML = `
            <svg class="spinner" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="32">
                    <animate attributeName="stroke-dashoffset" dur="1s" values="32;0" repeatCount="indefinite"/>
                </circle>
            </svg>
            Generando...
        `;

        try {
            await generatePDFPreview(filtered, dateOption?.label || 'Todos', options);
            showNotification('Vista previa generada', 'success');
        } catch (error) {
            showNotification('Error al generar vista previa', 'error');
        } finally {
            previewBtn.disabled = false;
            previewBtn.innerHTML = originalContent;
        }
    });

    // Botón de descarga
    const downloadBtn = document.getElementById('btn-download-pdf');
    downloadBtn?.addEventListener('click', async () => {
        const options = getModalOptions();
        const dateOption = DATE_OPTIONS.find(opt => opt.id === options.dateRange);
        const filtered = applyAllFilters(products, options);

        if (filtered.length === 0) {
            showNotification('No hay productos con código de barras con estos filtros', 'warning');
            return;
        }

        // Mostrar estado de carga
        downloadBtn.disabled = true;
        downloadBtn.innerHTML = `
            <svg class="spinner" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="32">
                    <animate attributeName="stroke-dashoffset" dur="1s" values="32;0" repeatCount="indefinite"/>
                </circle>
            </svg>
            Generando PDF...
        `;

        try {
            const fileName = await generatePDF(filtered, dateOption?.label || 'Todos', options);
            showNotification(`PDF descargado: ${fileName}`, 'success');
            closeBarcodeModal();
        } catch (error) {
            showNotification('Error al generar el PDF', 'error');

            // Restaurar botón
            downloadBtn.disabled = false;
            downloadBtn.innerHTML = `
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="7 10 12 15 17 10"></polyline>
                    <line x1="12" y1="15" x2="12" y2="3"></line>
                </svg>
                Descargar PDF
            `;
        }
    });
}

/**
 * Genera una vista previa del PDF en una nueva ventana
 * @param {Array} products - Productos filtrados
 * @param {string} optionLabel - Etiqueta de la opción
 * @param {Object} options - Opciones de configuración
 */
async function generatePDFPreview(products, optionLabel, options) {
    if (typeof window.jspdf === 'undefined') {
        await loadJsPDF();
    }

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF('p', 'mm', options.pageSize || 'a4');

    // Generar el PDF con las mismas opciones
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    const margin = 12;
    const cols = options.columns || 2;
    const colWidth = (pageWidth - margin * 2) / cols;
    const barcodeWidth = colWidth - 15;
    const barcodeHeight = cols >= 4 ? 25 : (cols === 3 ? 30 : 35);

    let itemHeight = 15 + barcodeHeight;
    if (options.includeProductName) itemHeight += 8;
    if (options.includePrice) itemHeight += 6;
    if (options.includeCategory) itemHeight += 6;
    itemHeight += 5;

    let currentY = margin;
    let currentCol = 0;
    let cantProduct= await countFromApi('productos');
    // Solo mostrar primeros 6 productos como preview
    const previewProducts = products.slice(0, cantProduct);

    if (options.includeHeader) {
        doc.setFillColor(0, 91, 182);
        doc.rect(0, 0, pageWidth, 28, 'F');
        doc.setFontSize(20);
        doc.setFont('helvetica', 'bold');
        doc.setTextColor(255, 255, 255);
        doc.text('TALLER DE DIEGO - VISTA PREVIA', pageWidth / 2, 12, { align: 'center' });
        doc.setFontSize(10);
        doc.setFont('helvetica', 'normal');
        doc.text(`Mostrando ${previewProducts.length} de ${products.length} productos`, pageWidth / 2, 19, { align: 'center' });
        currentY = 40;
    }

    doc.setTextColor(0);

    for (let i = 0; i < previewProducts.length; i++) {
        const product = previewProducts[i];
        const x = margin + (currentCol * colWidth);

        doc.setDrawColor(220);
        doc.setFillColor(252, 252, 252);
        doc.roundedRect(x + 2, currentY - 2, colWidth - 6, itemHeight - 3, 2, 2, 'FD');

        let textY = currentY + 4;

        if (options.includeProductName) {
            doc.setFontSize(cols >= 4 ? 7 : (cols === 3 ? 8 : 9));
            doc.setFont('helvetica', 'bold');
            doc.setTextColor(44, 62, 80);
            const productName = truncateText(product.nombre || 'Sin nombre', cols >= 4 ? 20 : 30);
            doc.text(productName, x + 4, textY);
            textY += 6;
        }

        if (options.includeCategory && product.categoria) {
            doc.setFontSize(7);
            doc.setTextColor(100);
            doc.text(`Cat: ${product.categoria}`, x + 4, textY);
            textY += 4;
        }

        try {
            const barcodeDataUrl = await generateBarcodeDataUrl(product.codBarras, cols);
            if (barcodeDataUrl) {
                const imgX = x + (colWidth - barcodeWidth) / 2 - 1;
                doc.addImage(barcodeDataUrl, 'PNG', imgX, textY, barcodeWidth, barcodeHeight);
                textY += barcodeHeight + 2;
            }
        } catch (error) {
            textY += barcodeHeight + 2;
        }

        if (options.includePrice && product.precioVenta) {
            doc.setFontSize(8);
            doc.setFont('helvetica', 'bold');
            doc.setTextColor(0, 91, 182);
            doc.text(`S/ ${parseFloat(product.precioVenta).toFixed(2)}`, x + colWidth / 2, textY, { align: 'center' });
        }

        currentCol++;
        if (currentCol >= cols) {
            currentCol = 0;
            currentY += itemHeight;
        }
    }

    // Abrir en nueva ventana
    const pdfBlob = doc.output('blob');
    const pdfUrl = URL.createObjectURL(pdfBlob);
    window.open(pdfUrl, '_blank');
}

/**
 * Vincula el botón de códigos de barras al modal
 */
export function bindBarcodeButton() {
    const barcodeBtn = document.getElementById('barcode-btn');

    if (!barcodeBtn) {
        return;
    }

    barcodeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        openBarcodeModal();
    });
}
