export function validateField(input, message) {
  const errorElement = input.parentElement.querySelector(".error-message");
  if (errorElement) errorElement.remove();

  const value = input.value.trim();

  // Validar campo vacío o solo espacios
  if (!value) {
    showFieldError(input, message);
    return false;
  }

  // Validar caracteres repetitivos irrelevantes
  if (hasInvalidPatterns(value)) {
    showFieldError(input, "No se permiten caracteres repetitivos o símbolos irrelevantes");
    return false;
  }

  input.classList.remove("input-error");
  return true;
}

function showFieldError(input, message) {
  const span = document.createElement("span");
  span.classList.add("error-message");
  span.textContent = message;
  input.classList.add("input-error");
  input.parentElement.appendChild(span);
}

// Detecta patrones de caracteres irrelevantes
function hasInvalidPatterns(text) {
  // Patrones prohibidos
  const patterns = [
    /[►◄▲▼♦♣♠♥]+/g,           // Símbolos de flecha y cartas
    /[░▒▓█■□▪▫]+/g,           // Símbolos de bloques
    /[★☆♪♫♯♭]+/g,            // Símbolos musicales y estrellas
    /(.)\\1{4,}/g,             // 5 o más caracteres consecutivos iguales
    /[!@#$%^&*()+={}\\[\\]|\\:;"'<>?,.]{5,}/g, // 5 o más símbolos consecutivos
    /^\\s*[.\\-_~=+*#]{3,}\\s*$/g, // Solo símbolos decorativos
    /^[0-9]{10,}$/g,          // Solo números largos sin sentido
  ];

  return patterns.some(pattern => pattern.test(text));
}

export function validateFormData(form, formData, isAutopart) {
  let isValid = true;


  // Validar nombre del producto
  const nameValid = validateProductName(form['product-name'], formData.nombre);
  if (!nameValid) {
    isValid = false;
  }

  // Validar marca
  const brandValid = validateBrand(form['product-brand'], formData.marca);
  if (!brandValid) {
    isValid = false;
  }

  // Validar categoría
  if (!formData.categoria) {
    validateField(form['product-category'], "Selecciona una categoría");
    isValid = false;
  }

  // Validar números (stock, precios)
  const numbersValid = validateNumbers(form, formData);
  if (!numbersValid) {
    isValid = false;
  }

  // Validar descripción
  const descValid = validateDescription(form['product-description'], formData.descripcion);
  if (!descValid) {
    isValid = false;
  }

  // Validar campos de autopartes si aplica
  if (isAutopart) {
    const autopartValid = validateAutopartFields(form, formData);
    if (!autopartValid) {
      isValid = false;
    }
  }

  return isValid;
}

// Validaciones específicas por tipo de campo
function validateProductName(input, value) {
  if (!value || !value.trim()) {
    validateField(input, "El nombre del producto es obligatorio");
    return false;
  }

  if (value.length < 2) {
    validateField(input, "El nombre debe tener al menos 2 caracteres");
    return false;
  }

  if (!/^[a-zA-ZñÑáéíóúÁÉÍÓÚüÜ0-9\s\-.,()]+$/.test(value)) {
    validateField(input, "El nombre solo puede contener letras, números y signos básicos");
    return false;
  }

  // Si pasa todas las validaciones, limpiar errores
  const errorElement = input.parentElement.querySelector(".error-message");
  if (errorElement) errorElement.remove();
  input.classList.remove("input-error");
  
  return true;
}

function validateBrand(input, value) {
  if (!value || !value.trim()) {
    validateField(input, "La marca es obligatoria");
    return false;
  }

  if (!/^[a-zA-ZñÑáéíóúÁÉÍÓÚüÜ0-9\s\-&.]+$/.test(value)) {
    validateField(input, "La marca solo puede contener letras, números y símbolos básicos");
    return false;
  }

  // Si pasa todas las validaciones, limpiar errores
  const errorElement = input.parentElement.querySelector(".error-message");
  if (errorElement) errorElement.remove();
  input.classList.remove("input-error");
  
  return true;
}

function validateNumbers(form, formData) {
  let isValid = true;

  // Validar stock
  if (isNaN(formData.stock) || formData.stock < 0) {
    validateField(form['product-stock'], "El stock debe ser un número positivo");
    isValid = false;
  }

  // Validar stock mínimo
  if (isNaN(formData.stockMin) || formData.stockMin < 0) {
    validateField(form['product-min-stock'], "El stock mínimo debe ser un número positivo");
    isValid = false;
  }

  // Validar precios
  if (isNaN(formData.precioCompra) || formData.precioCompra <= 0) {
    validateField(form['product-purchase-price'], "El precio de compra debe ser mayor a 0");
    isValid = false;
  }

  if (isNaN(formData.precioVenta) || formData.precioVenta <= 0) {
    validateField(form['product-selling-price'], "El precio de venta debe ser mayor a 0");
    isValid = false;
  }

  // Validar lógica de precios
  if (formData.precioVenta <= formData.precioCompra) {
    validateField(form['product-selling-price'], "El precio de venta debe ser mayor al de compra");
    isValid = false;
  }

  return isValid;
}

function validateDescription(input, value) {
  if (value && value.trim()) {
    if (value.length < 10) {
      validateField(input, "La descripción debe tener al menos 10 caracteres si se proporciona");
      return false;
    }

    // Permitir solo texto descriptivo normal
    if (!/^[a-zA-ZñÑáéíóúÁÉÍÓÚüÜ0-9\s\-.,()\n\r]+$/.test(value)) {
      validateField(input, "La descripción solo puede contener texto descriptivo normal");
      return false;
    }
  }

  return true;
}

function validateAutopartFields(form, formData) {
  let isValid = true;

  if (!formData.modelo || !formData.modelo.trim()) {
    validateField(form['product-model'], "El modelo compatible es obligatorio para autopartes");
    isValid = false;
  } else if (!/^[a-zA-ZñÑáéíóúÁÉÍÓÚüÜ0-9\s\-,.()]+$/.test(formData.modelo)) {
    validateField(form['product-model'], "El modelo solo puede contener letras, números y símbolos básicos");
    isValid = false;
  }

  // Validación completa de años
  const yearValidation = validateYearField(formData.anio);
  if (!yearValidation.isValid) {
    showFieldError(form['product-year'], yearValidation.message);
    form['product-year'].classList.add("input-error");
    isValid = false;
  }

  return isValid;
}

/**
 * Valida el campo de años compatibles para autopartes
 * Formatos válidos:
 * - Año único: "2020"
 * - Rango: "2018-2023"
 * - Lista: "2018, 2020, 2022"
 * - Mixto: "2015-2018, 2020, 2022-2024"
 * 
 * @param {string} value - Valor del campo de año
 * @returns {{isValid: boolean, message: string}} Resultado de validación
 */
function validateYearField(value) {
  const currentYear = new Date().getFullYear();
  const minYear = 1950; // Año mínimo razonable para autopartes
  const maxYear = currentYear + 1; // Permitir hasta el próximo año

  // Validar campo vacío
  if (!value || !value.trim()) {
    return { isValid: false, message: "El año compatible es obligatorio para autopartes" };
  }

  const cleanValue = value.trim();

  // Validar formato básico: solo números, comas, guiones y espacios
  if (!/^[0-9\s,\-]+$/.test(cleanValue)) {
    return { isValid: false, message: "Solo se permiten números, comas y guiones (ej: 2020-2023)" };
  }

  // Validar que no haya guiones o comas duplicados/mal formados
  if (/[\-]{2,}|[,]{2,}|^[\-,]|[\-,]$|,\s*,|\-\s*\-/.test(cleanValue)) {
    return { isValid: false, message: "Formato inválido: revisa los guiones y comas" };
  }

  // Separar por comas para procesar cada segmento
  const segments = cleanValue.split(',').map(s => s.trim()).filter(s => s);

  if (segments.length === 0) {
    return { isValid: false, message: "Debes ingresar al menos un año válido" };
  }

  for (const segment of segments) {
    // Verificar si es un rango (contiene guión)
    if (segment.includes('-')) {
      const parts = segment.split('-').map(p => p.trim()).filter(p => p);

      // Validar que el rango tenga exactamente 2 partes
      if (parts.length !== 2) {
        return { isValid: false, message: `Rango inválido: "${segment}". Usa formato: 2020-2023` };
      }

      const startYear = parseInt(parts[0], 10);
      const endYear = parseInt(parts[1], 10);

      // Validar que ambos sean números válidos
      if (isNaN(startYear) || isNaN(endYear)) {
        return { isValid: false, message: `Años inválidos en rango: "${segment}"` };
      }

      // Validar rango de años válidos
      if (startYear < minYear || endYear < minYear) {
        return { isValid: false, message: `Año muy antiguo. Mínimo permitido: ${minYear}` };
      }

      if (startYear > maxYear || endYear > maxYear) {
        return { isValid: false, message: `Año futuro inválido. Máximo permitido: ${maxYear}` };
      }

      // Validar que inicio <= fin
      if (startYear > endYear) {
        return { isValid: false, message: `Rango invertido: "${segment}". El año inicial debe ser menor o igual al final` };
      }

      // Validar longitud del rango (evitar rangos absurdos como 1950-2025)
      if (endYear - startYear > 30) {
        return { isValid: false, message: `Rango muy amplio: "${segment}". Máximo 30 años de diferencia` };
      }

    } else {
      // Es un año único
      const year = parseInt(segment, 10);

      if (isNaN(year)) {
        return { isValid: false, message: `Año inválido: "${segment}"` };
      }

      // Validar que sea un año de 4 dígitos
      if (segment.length !== 4) {
        return { isValid: false, message: `Formato de año incorrecto: "${segment}". Usa 4 dígitos (ej: 2020)` };
      }

      if (year < minYear) {
        return { isValid: false, message: `Año muy antiguo: ${year}. Mínimo permitido: ${minYear}` };
      }

      if (year > maxYear) {
        return { isValid: false, message: `Año futuro inválido: ${year}. Máximo permitido: ${maxYear}` };
      }
    }
  }

  return { isValid: true, message: "" };
}