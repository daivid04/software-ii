import { createResource, updateResource, fetchFromApi } from "../../data-manager.js";
import { showNotification } from "../../utils/notification.js";
import { uploadImage, updateImage, compressImage } from "../../utils/store/manager-image.js";
import { closeModalForm } from "./modal-product.js";
import { renderProducts } from "../product-list/product-list.js";
import { generateBarcodeImage, downloadBarcodeImage, isValidBarcode } from "../../utils/codbarra.js";
import { validateFormData } from "./modal-validation.js";

// ========================================
// UTILIDADES DE SANITIZACIÓN
// ========================================

function sanitizeText(value, { allowNewLines = false } = {}) {
  if (value === undefined || value === null) {
    return "";
  }

  let text = String(value)
    .replace(/<[^>]*?>/g, "") // eliminar etiquetas HTML
    .replace(/[`$]/g, "") // remover caracteres susceptibles a plantillas/script
    .replace(/[\u0000-\u001F\u007F-\u009F]/g, " "); // caracteres de control

  if (allowNewLines) {
    text = text.replace(/[\t\u00A0]+/g, " ");
  } else {
    text = text.replace(/\s+/g, " ");
  }

  return text.trim();
}

function containsForbiddenContent(value) {
  if (value === undefined || value === null) {
    return false;
  }

  const text = String(value).toLowerCase();

  // patrones básicos de XSS/HTML
  if (/<\s*script|<\s*\/script|javascript:/i.test(text)) {
    return true;
  }

  if (/<[^>]+>/g.test(text)) {
    return true;
  }

  return false;
}

// ========================================
// GENERADOR DE CÓDIGOS DE BARRAS
// ========================================

/**
 * Genera un código de barras único con el formato: T-A001-CAT (Base-26 alfanumérica)
 * Verifica que no exista en la base de datos antes de retornarlo
 * 
 * Formato: T-[LETRAS][NÚMEROS]-[CATEGORÍA]
 * - T: Prefijo del taller
 * - A-ZZ: Secuencia alfanumérica base-26 (A, B, ..., Z, AA, AB, ..., ZZ)
 * - 001-999: Número secuencial con padding de 3 dígitos
 * - CAT: Código de 3 letras de la categoría
 * 
 * Capacidad: 675,999 combinaciones (26 letras simples + 676 letras dobles × 999 números)
 * 
 * Secuencia de ejemplo:
 * - A001 a A999 (999 productos)
 * - B001 a Z999 (25 × 999 = 24,975 productos)
 * - AA001 a AZ999 (26 × 999 = 25,974 productos)
 * - BA001 a ZZ999 (650 × 999 = 649,350 productos)
 * 
 * @param {string} categoria - Categoría del producto (ej: "Filtros", "Aceites")
 * @param {number} lastId - Último ID registrado en la base de datos
 * @param {Array} existingBarcodes - Array de códigos existentes para verificar unicidad
 * @returns {string} Código de barras único generado (ej: "T-A001-FIL")
 * 
 * @example
 * generateBarcode("Filtros", 0, [])    // "T-A001-FIL"
 * generateBarcode("Aceites", 999, [])  // "T-B001-ACE"
 * generateBarcode("Filtros", 25999, []) // "T-AA001-FIL"
 */
function generateBarcode(categoria, lastId, existingBarcodes = []) {
  // Prefijo fijo del taller
  const prefix = "T";

  // Generar sufijo de 3 letras basado en la categoría
  const categorySuffix = getCategorySuffix(categoria);

  let attempts = 0;
  const maxAttempts = 100; // Límite de intentos para evitar bucles infinitos

  // Intentar generar un código único
  while (attempts < maxAttempts) {
    const totalNumber = lastId + 1 + attempts;

    // Convertir a sistema base-26 alfanumérico
    // Secuencia: A001-A999, B001-B999, ..., Z001-Z999, AA001-AA999, ..., ZZ999
    const lettersAndNumber = convertToBase26(totalNumber);

    // Formato final: T-A001-FIL
    const barcode = `${prefix}-${lettersAndNumber}-${categorySuffix}`;

    // Verificar si el código ya existe
    if (!existingBarcodes.includes(barcode)) {
      return barcode;
    }

    attempts++;
  }

  // Si después de 100 intentos no se encuentra un código único, agregar timestamp
  const timestamp = Date.now().toString().slice(-3);
  const randomLetter = String.fromCharCode(65 + Math.floor(Math.random() * 26));
  const fallbackBarcode = `${prefix}-${randomLetter}${timestamp}-${categorySuffix}`;
  return fallbackBarcode;
}

/**
 * Convierte un número a formato base-26 alfanumérico (A001-ZZ999)
 * 
 * @param {number} num - Número a convertir (1-675999)
 * @returns {string} Código en formato base-26 (ej: "A001", "B342", "AA001", "ZZ999")
 * 
 * @example
 * convertToBase26(1)     // "A001"
 * convertToBase26(999)   // "A999"
 * convertToBase26(1000)  // "B001"
 * convertToBase26(25999) // "Z999"
 * convertToBase26(26000) // "AA001"
 */
function convertToBase26(num) {
  // Cada letra cubre 999 números
  const numbersPerLetter = 999;

  // Calcular índice de letra (0-based)
  const letterIndex = Math.floor((num - 1) / numbersPerLetter);

  // Calcular el número dentro del grupo (1-999)
  const numberPart = ((num - 1) % numbersPerLetter) + 1;

  // Convertir índice a letras (A, B, ..., Z, AA, AB, ..., ZZ)
  let letters = '';
  if (letterIndex < 26) {
    // Letras simples: A-Z (índices 0-25)
    letters = String.fromCharCode(65 + letterIndex);
  } else {
    // Letras dobles: AA-ZZ (índices 26+)
    const doubleIndex = letterIndex - 26;
    const firstLetter = String.fromCharCode(65 + Math.floor(doubleIndex / 26));
    const secondLetter = String.fromCharCode(65 + (doubleIndex % 26));
    letters = firstLetter + secondLetter;
  }

  // Formatear número con padding de 3 dígitos
  const formattedNumber = numberPart.toString().padStart(3, '0');

  return `${letters}${formattedNumber}`;
}

/**
 * Obtiene un sufijo de 3 letras basado en la categoría del producto
 * 
 * @param {string} categoria - Nombre de la categoría
 * @returns {string} Sufijo de 3 letras en mayúsculas
 * 
 * @example
 * getCategorySuffix("Filtros")        // "FIL"
 * getCategorySuffix("Aceites")        // "ACE"
 * getCategorySuffix("Llantas")        // "LLA"
 * getCategorySuffix("Herramientas")   // "HER"
 */
function getCategorySuffix(categoria) {
  // Mapeo de categorías comunes a códigos de 3 letras
  const categoryMap = {
    'Filtros': 'FIL',
    'Aceites': 'ACE',
    'Llantas': 'LLA',
    'Baterías': 'BAT',
    'Frenos': 'FRE',
    'Lubricantes': 'LUB',
    'Herramientas': 'HER',
    'Repuestos': 'REP',
    'Accesorios': 'ACC',
    'Iluminación': 'ILU',
    'Eléctricos': 'ELE',
    'Suspensión': 'SUS',
    'Motor': 'MOT',
    'Transmisión': 'TRA',
    'Refrigeración': 'REF',
    'Combustible': 'COM',
    'Escape': 'ESC',
    'Carrocería': 'CAR',
    'Limpieza': 'LIM',
    'Seguridad': 'SEG'
  };

  // Si la categoría existe en el mapa, usar ese código
  if (categoryMap[categoria]) {
    return categoryMap[categoria];
  }

  // Si no, generar código a partir de las primeras 3 letras
  // Eliminar espacios y acentos, convertir a mayúsculas
  const cleanCategory = categoria
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "") // Eliminar acentos
    .replace(/\s+/g, "") // Eliminar espacios
    .toUpperCase()
    .substring(0, 3);

  return cleanCategory || 'GEN'; // 'GEN' para "General" si falla
}

/**
 * Obtiene el último ID de producto registrado en la base de datos
 * 
 * @returns {Promise<number>} El ID más alto encontrado, o 0 si no hay productos
 * 
 * @example
 * const lastId = await getLastProductId(); // 45
 */
async function getLastProductId() {
  try {
    // Obtener todos los productos de la base de datos
    const productos = await fetchFromApi('productos');

    if (!productos || productos.length === 0) {
      return 0;
    }

    // Encontrar el ID más alto
    const maxId = Math.max(...productos.map(p => p.id));

    return maxId;
  } catch (error) {
    return 0;
  }
}

/**
 * Obtiene todos los códigos de barras existentes en la base de datos
 * para verificar unicidad al generar nuevos códigos
 * 
 * @returns {Promise<Array<string>>} Array de códigos de barras existentes
 * 
 * @example
 * const existingBarcodes = await getExistingBarcodes();
 * // ["TALLER-00001-FIL", "TALLER-00002-ACE", ...]
 */
async function getExistingBarcodes() {
  try {
    // Obtener todos los productos de la base de datos
    const productos = await fetchFromApi('productos');

    if (!productos || productos.length === 0) {
      return [];
    }

    // Filtrar solo los códigos de barras que no sean null o vacíos
    const barcodes = productos
      .map(p => p.codBarras)
      .filter(code => code != null && code !== '');


    // Mostrar algunos ejemplos en consola para debug
    if (barcodes.length > 0) {
    }

    return barcodes;
  } catch (error) {
    return [];
  }
}



export function setupModalEvents(type = 'add', productId = null) {
  const modalOverlay = document.querySelector(".modal-overlay");
  const form = document.getElementById('form-product');
  const btnCancel = document.querySelector('.btn-cancel');
  const btnClose = document.querySelector('.modal-close');
  const autopartCheckbox = document.getElementById('product-autopart');

  //Seguridad de datos de entrada

  setupInputNumber();
  setupInputNumberWithCustomLimits();
  setupTextInputValidation(); // Nueva función para validar texto en tiempo real
  setupCloseHandlers(modalOverlay, btnCancel, btnClose);
  setupAutopartToggle(autopartCheckbox);
  setupPreviewImage('product-img', 'product-preview');

  // Configurar código de barras si existe (solo en modo view/edit)
  if (type === 'view' || type === 'edit') {
    setupBarcodeDisplay(productId);
  }

  // Solo configurar submit si NO es modo view
  if (type !== 'view') {
    setupFormSubmit(form, autopartCheckbox, type, productId);
  }
}

function setupAutopartToggle(autopartCheckbox) {
  const autopartFields = document.querySelector("[data-autopart-fields]");


  const toggleAutopartFields = () => {
    if (!autopartCheckbox) return;

    const show = autopartCheckbox.checked;
    autopartFields?.classList.toggle("is-visible", show);

    autopartFields?.querySelectorAll("input").forEach((input) => {
      input.disabled = !show;
      if (!show) {
        input.value = "";
      }
    });
  }


  if (autopartCheckbox) {
    toggleAutopartFields();
    autopartCheckbox.addEventListener("change", toggleAutopartFields);
  }
}

function setupCloseHandlers(modalOverlay, btnCancel, btnClose) {
  const closeHandlers = () => closeModalForm();
  btnClose?.addEventListener("click", closeHandlers);
  btnCancel?.addEventListener("click", closeHandlers);

  modalOverlay?.addEventListener("click", (event) => {
    if (event.target === modalOverlay) {
      closeHandlers();
    }
  });

  const escapeHandler = (event) => {
    if (event.key === "Escape") {
      closeHandlers();
      document.removeEventListener("keydown", escapeHandler);
    }
  }
  document.addEventListener("keydown", escapeHandler);
}

function setupFormSubmit(form, autopartCheckbox, type = 'add', productId = null) {
  let isEdit = (type === 'edit' && productId !== null);
  let endpoint = "productos";
  form?.addEventListener('submit', async (e) => {
    e.preventDefault();

    // DATOS DEL FORMULARIO (sanitizados)
    const rawNombre = form['product-name'].value;
    const rawMarca = form['product-brand'].value;
    const rawCategoria = form['product-category'].value;
    const rawDescripcion = form['product-description'].value;

    const rawFields = {
      nombre: rawNombre,
      marca: rawMarca,
      descripcion: rawDescripcion,
      modelo: form['product-model']?.value,
    };

    const fieldWithForbiddenContent = Object.entries(rawFields)
      .find(([, value]) => containsForbiddenContent(value));

    if (fieldWithForbiddenContent) {
      const [fieldName] = fieldWithForbiddenContent;
      showNotification('El campo no puede contener etiquetas HTML o script.', 'error');
      return;
    }

    let formData = {
      nombre: sanitizeText(rawNombre),
      marca: sanitizeText(rawMarca),
      categoria: sanitizeText(rawCategoria),
      stock: parseInt(form['product-stock'].value, 10) || 0,
      stockMin: parseInt(form['product-min-stock'].value, 10) || 0,
      precioCompra: parseFloat(form['product-purchase-price'].value) || 0,
      precioVenta: parseFloat(form['product-selling-price'].value) || 0,
      descripcion: sanitizeText(rawDescripcion, { allowNewLines: true }),
    };

    // ========================================
    // GENERACIÓN AUTOMÁTICA DE CÓDIGO DE BARRAS ÚNICO
    // Solo para productos nuevos (no edición)
    // ========================================
    if (!isEdit) {
      try {
        // Paso 1: Obtener el último ID
        const lastId = await getLastProductId();

        // Paso 2: Obtener todos los códigos existentes para verificar unicidad
        const existingBarcodes = await getExistingBarcodes();

        // Paso 3: Generar código único (verifica que no exista en BD)
        const barcode = generateBarcode(formData.categoria, lastId, existingBarcodes);

        // Paso 4: Asignar al producto
        formData.codBarras = barcode;
      } catch (error) {
        showNotification('Error al generar código de barras único', 'error');
        return; // Detener el envío si falla la generación
      }
    }

    const isAutopart = autopartCheckbox?.checked ?? false;

    if (isAutopart) {
      formData.modelo = sanitizeText(form['product-model'].value);
      formData.anio = form['product-year'].value; // Mantener como string para validación
      endpoint = "autopartes";
    }

    // ========================================
    // VALIDACIÓN COMPLETA DEL FORMULARIO
    // ========================================
    if (!validateFormData(form, formData, isAutopart)) {
      showNotification('Por favor corrige los errores en el formulario', 'error');
      return; // Detener el envío si hay errores de validación
    }

    // El año ya está validado como string (soporta rangos: "2018-2023" o listas: "2018, 2020")
    // No convertir a número, mantener como string

    // ENVIO DE DATOS
    try {
      const imgInput = document.getElementById('product-img');
      const imageFile = imgInput?.files[0];
      const imageCompress = await compressImage(imageFile, {
        maxWidth: 1200,
        maxHeight: 1200,
        quality: 0.8,
        maxSizeBytes: 5 * 1024 * 1024
      })

      if (isEdit) {
        await updateResource(endpoint, productId, formData);


        if (imageFile) {
          const imgName = await updateImage(productId, imageCompress, 'productos', 'productos');
          formData.img = imgName;
          await updateResource(endpoint, productId, formData);
        }
        showNotification("Producto actualizado exitosamente", "success");
      } else {
        const newProduct = await createResource(endpoint, formData);

        if (imageCompress) {
          const imgName = await uploadImage(imageCompress, newProduct.id, 'productos');
          formData.img = imgName;
          await updateResource(endpoint, newProduct.id, formData);

        }
        showNotification(`Producto agregado exitosamente.`, "success");
      }

      closeModalForm();
      await renderProducts(null, true);

    } catch (error) {
      showNotification("Error al crear producto: " + error.message, "error");
    }
  });
}


async function setupPreviewImage(inputId, previewId) {
  const input = document.getElementById(inputId);
  const previewImg = document.getElementById(previewId);
  const fileNameSpan = document.getElementById('file-name');

  if (!input || !previewImg) {
    return;
  }

  input.addEventListener('change', async () => {
    const file = input.files[0];

    if (!file) {
      previewImg.style.display = 'none';
      previewImg.classList.remove('show');
      if (fileNameSpan) fileNameSpan.textContent = 'Ningún archivo seleccionado';
      return;
    }

    const validTypes = ['image/jpg', 'image/jpeg', 'image/png', 'image/webp'];
    if (!validTypes.includes(file.type)) {
      showNotification('Solo se permiten imágenes JPG, JPEG, PNG y WEBP', "info");
      input.value = '';
      previewImg.style.display = 'none';
      previewImg.classList.remove('show');
      if (fileNameSpan) fileNameSpan.textContent = 'Ningún archivo seleccionado';
      return;
    }

    const maxSize = 5 * 1024 * 1024; // 5MB
    let fileToShow = file;

    if (file.size > maxSize) {
      showNotification('La imagen supera 5MB, se comprimirá automáticamente para vista previa', 'info');
      try {
        fileToShow = await compressImage(file, {
          maxWidth: 1200,
          maxHeight: 1200,
          quality: 0.75,
          maxSizeBytes: maxSize
        });
      } catch (err) {
        showNotification('Error al comprimir imagen', 'error');
        input.value = '';
        return;
      }
    }

    if (fileNameSpan) fileNameSpan.textContent = fileToShow.name || file.name;
    previewImg.src = URL.createObjectURL(fileToShow);
    previewImg.style.display = 'block';
    previewImg.classList.add('show');
  });
}


function setupInputNumber() {
  const numberInputs = document.querySelectorAll('input[type="number"]');

  numberInputs.forEach(input => {
    // Validar en el evento "input"
    input.addEventListener('input', (e) => {
      const value = e.target.value;


      const sanitizedValue = value.replace(/[^0-9.]/g, ''); // Eliminar caracteres no numéricos
      const parts = sanitizedValue.split('.'); // Dividir por el punto decimal

      e.target.value = parts.length > 2
        ? `${parts[0]}.${parts.slice(1).join('')}`
        : sanitizedValue;
    });

    input.addEventListener('keydown', (e) => {
      const allowedKeys = [
        'Backspace', 'Tab', 'ArrowLeft', 'ArrowRight', 'Delete', 'Enter', // Teclas de navegación
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.' // Números y punto decimal
      ];

      // Prevenir teclas no permitidas
      if (!allowedKeys.includes(e.key) && !e.ctrlKey && !e.metaKey) {
        e.preventDefault();
      }

      // Prevenir múltiples puntos decimales
      if (e.key === '.' && e.target.value.includes('.')) {
        e.preventDefault();
      }
    });
  });
}


function setupInputNumberWithCustomLimits() {
  // Configurar límites específicos para cada campo
  const fieldLimits = {
    'product-stock': 1000,
    'product-min-stock': 1000, // Límite máximo para el stock
    'product-purchase-price': 10000000, // Límite máximo para el precio de compra
    'product-selling-price': 10000000 // Límite máximo para el precio de venta
  };

  // Seleccionar todos los campos de tipo number
  const numberInputs = document.querySelectorAll('input[type="number"]');

  numberInputs.forEach(input => {
    const maxValue = fieldLimits[input.id]; // Obtener el límite según el id del campo

    if (maxValue) {
      // Validar en el evento "input"
      input.addEventListener('input', (e) => {
        const value = parseFloat(e.target.value);

        // Si el valor supera el máximo, ajustarlo al máximo permitido
        if (value > maxValue) {
          e.target.value = maxValue;
          showNotification(`El valor no puede ser mayor a ${maxValue}`, "warning");
        }
      });

      // Validar en el evento "keydown"
      input.addEventListener('keydown', (e) => {
        const allowedKeys = [
          'Backspace', 'Tab', 'ArrowLeft', 'ArrowRight', 'Delete', 'Enter', // Teclas de navegación
          '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.' // Números y punto decimal
        ];

        // Prevenir teclas no permitidas
        if (!allowedKeys.includes(e.key) && !e.ctrlKey && !e.metaKey) {
          e.preventDefault();
        }

        // Prevenir múltiples puntos decimales
        if (e.key === '.' && e.target.value.includes('.')) {
          e.preventDefault();
        }
      });
    }
  });
}

// ========================================
// CONFIGURACIÓN DE CÓDIGO DE BARRAS
// ========================================

/**
 * Configura la visualización y descarga del código de barras en el modal
 * Solo se ejecuta si el producto tiene código asignado
 * 
 * @param {number} productId - ID del producto
 */
async function setupBarcodeDisplay(productId) {
  try {
    if (typeof JsBarcode === 'undefined') {
      return;
    }

    const producto = await fetchFromApi('productos', productId);
    if (!producto || !producto.codBarras) return;


    if (!isValidBarcode(producto.codBarras)) {
      return;
    }

    generateBarcodeImage('product-barcode', producto.codBarras, producto.nombre);

    const container = document.getElementById('barcode-container');
    if (container) {
      container.addEventListener('click', async () => {
        const downloaded = await downloadBarcodeImage(producto.codBarras, producto.nombre);
        if (downloaded) {
          showNotification(`Código descargado: ${producto.codBarras}`, 'success');
        }
      });
    }
  } catch (error) {
  }
}

// ========================================
// VALIDACIÓN DE CAMPOS DE TEXTO EN TIEMPO REAL
// ========================================

/**
 * Configura validación en tiempo real para campos de texto
 * Previene caracteres irrelevantes y espacios múltiples
 */
function setupTextInputValidation() {
  const textInputs = document.querySelectorAll('input[type="text"], textarea');

  textInputs.forEach(input => {
    // Validación en tiempo real mientras se escribe
    input.addEventListener('input', (e) => {
      let value = e.target.value;

      // Limpiar caracteres irrelevantes inmediatamente
      value = cleanInvalidCharacters(value, input.id);

      // Limitar espacios múltiples
      value = value.replace(/\s{3,}/g, '  '); // Máximo 2 espacios consecutivos

      // Actualizar valor si cambió
      if (value !== e.target.value) {
        e.target.value = value;
        showTemporaryWarning(input, "Algunos caracteres fueron removidos automáticamente");
      }

      // Limpiar mensajes de error previos si el campo ahora es válido
      clearFieldError(input);
    });

    // Validación final al salir del campo
    input.addEventListener('blur', (e) => {
      const value = e.target.value.trim();

      if (value && hasInvalidPatterns(value)) {
        showFieldError(input, "Contiene caracteres no permitidos");
      }

      // Limpiar espacios al inicio y final
      e.target.value = value;
    });

    // Prevenir pegado de contenido peligroso
    input.addEventListener('paste', (e) => {
      setTimeout(() => {
        let value = e.target.value;
        value = cleanInvalidCharacters(value, input.id);
        value = value.replace(/\s{3,}/g, '  ');
        e.target.value = value;
      }, 10);
    });
  });
}

/**
 * Limpia caracteres no válidos según el tipo de campo
 */
function cleanInvalidCharacters(value, inputId) {
  // Reglas específicas por campo
  switch (inputId) {
    case 'product-name':
    case 'product-brand':
    case 'product-model':
      // Solo letras, números, espacios y signos básicos
      return value.replace(/[^a-zA-ZñÑáéíóúÁÉÍÓÚüÜ0-9\s\-.,()&]/g, '');

    case 'product-year':
      // Solo números, espacios, comas y guiones
      return value.replace(/[^0-9\s,\-]/g, '');

    case 'product-description':
      // Texto descriptivo normal
      return value.replace(/[^a-zA-ZñÑáéíóúÁÉÍÓÚüÜ0-9\s\-.,()\n\r]/g, '');

    default:
      // Limpieza general: remover símbolos irrelevantes
      return value.replace(/[►◄▲▼♦♣♠♥░▒▓█■□▪▫★☆♪♫♯♭]/g, '');
  }
}

/**
 * Muestra un aviso temporal que desaparece automáticamente
 */
function showTemporaryWarning(input, message) {
  const existingWarning = input.parentElement.querySelector('.temp-warning');
  if (existingWarning) {
    existingWarning.remove();
  }

  const warning = document.createElement('span');
  warning.classList.add('temp-warning');
  warning.textContent = message;
  warning.style.cssText = `
    color: #ff9800; 
    font-size: 12px; 
    margin-top: 4px; 
    display: block;
    opacity: 1;
    transition: opacity 0.3s ease;
  `;

  input.parentElement.appendChild(warning);

  // Desvanecer y remover después de 3 segundos
  setTimeout(() => {
    warning.style.opacity = '0';
    setTimeout(() => warning.remove(), 300);
  }, 3000);
}

/**
 * Limpia mensajes de error de un campo
 */
function clearFieldError(input) {
  const errorElement = input.parentElement.querySelector('.error-message');
  if (errorElement) {
    errorElement.remove();
  }
  input.classList.remove('input-error');
}

/**
 * Detecta patrones de caracteres irrelevantes (función importada de modal-validation.js)
 */
function hasInvalidPatterns(text) {
  const patterns = [
    /[►◄▲▼♦♣♠♥]+/g,
    /[░▒▓█■□▪▫]+/g,
    /[★☆♪♫♯♭]+/g,
    /(.)\\1{4,}/g,
    /[!@#$%^&*()+={}\\[\\]|\\:;"'<>?,.]{5,}/g,
    /^\\s*[.\\-_~=+*#]{3,}\\s*$/g,
    /^[0-9]{10,}$/g,
  ];

  return patterns.some(pattern => pattern.test(text));
}

/**
 * Muestra error en un campo específico
 */
function showFieldError(input, message) {
  clearFieldError(input);

  const span = document.createElement("span");
  span.classList.add("error-message");
  span.textContent = message;
  input.classList.add("input-error");
  input.parentElement.appendChild(span);
}

