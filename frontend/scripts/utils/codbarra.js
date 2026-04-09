/**
 * ========================================
 * UTILIDADES PARA CÓDIGOS DE BARRAS
 * ========================================
 * 
 * Funciones para generar y descargar códigos de barras usando JsBarcode
 */

/**
 * Genera un código de barras en formato SVG y lo renderiza en un elemento
 * 
 * @param {string} elementId - ID del elemento donde renderizar
 * @param {string} barcodeValue - Valor del código de barras
 * @param {string} productName - Nombre del producto (no usado actualmente)
 * @returns {boolean} true si se generó correctamente
 * 
 * @example
 * generateBarcodeImage('product-barcode', 'T-A001-FIL');
 */
export function generateBarcodeImage(elementId, barcodeValue, productName = '') {
    try {
        if (typeof JsBarcode === 'undefined') {
            return false;
        }

        if (!barcodeValue || barcodeValue.trim() === '') {
            return false;
        }

        const element = document.getElementById(elementId);
        if (!element) {
            return false;
        }

        const options = {
            format: 'CODE128',
            width: 1.3,
            height: 80,
            displayValue: true,
            text: barcodeValue,
            fontSize: 14,
            fontOptions: 'bold',
            textAlign: 'center',
            textMargin: 8,
            margin: 12,
            background: '#ffffff',
            lineColor: '#000000',
            valid: (valid) => {
                if (!valid) {
                }
            }
        };

        // Generar el código de barras
        JsBarcode(element, barcodeValue, options);

        return true;

    } catch (error) {
        return false;
    }
}

/**
 * Descarga el código de barras como imagen PNG
 * 
 * @param {string} barcodeValue - Valor del código de barras
 * @param {string} productName - Nombre del producto (usado en nombre del archivo)
 * @returns {Promise<boolean>} true si se descargó correctamente
 * 
 * @example
 * await downloadBarcodeImage('T-A001-FIL', 'Filtro de Aceite');
 * // Descarga: filtro_de_aceite.png
 */
export async function downloadBarcodeImage(barcodeValue, productName = 'producto') {
    try {

        // Validaciones
        if (!barcodeValue || barcodeValue.trim() === '') {
            throw new Error('Código de barras vacío');
        }

        if (typeof JsBarcode === 'undefined') {
            throw new Error('JsBarcode no está cargado');
        }

        // Crear un canvas temporal para generar la imagen
        const tempCanvas = document.createElement('canvas');

        // Calcular ancho dinámico del canvas
        const barcodeLength = barcodeValue.length;
        const barWidth = 2.5;
        const estimatedModules = (barcodeLength + 3) * 11;
        const barcodeWidth = estimatedModules * barWidth;
        const lateralMargin = 40;
        const canvasWidth = Math.ceil(barcodeWidth + lateralMargin);
        const canvasHeight = 150;

        tempCanvas.width = canvasWidth;
        tempCanvas.height = canvasHeight;

        // Generar el código de barras
        JsBarcode(tempCanvas, barcodeValue, {
            format: 'CODE128',
            width: barWidth,
            height: 90,
            displayValue: true,
            fontSize: 16,
            fontOptions: 'bold',
            textAlign: 'center',
            textMargin: 5,
            margin: 20,
            background: '#ffffff',
            lineColor: '#000000'
        });

        // Canvas final con nombre del producto
        const finalCanvas = document.createElement('canvas');
        const ctx = finalCanvas.getContext('2d');

        finalCanvas.width = canvasWidth;
        finalCanvas.height = canvasHeight + 30;

        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, finalCanvas.width, finalCanvas.height);
        ctx.drawImage(tempCanvas, 0, 0);

        // Agregar nombre del producto
        if (productName && productName.trim() !== '') {
            ctx.fillStyle = '#2c3e50';
            ctx.font = 'bold 16px Arial, sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';

            const maxLength = 40;
            const displayName = productName.length > maxLength
                ? productName.substring(0, maxLength) + '...'
                : productName;

            ctx.fillText(displayName, canvasWidth / 2, canvasHeight + 18);
        }

        // Convertir a PNG
        const blob = await new Promise((resolve, reject) => {
            finalCanvas.toBlob((blob) => {
                if (blob) {
                    resolve(blob);
                } else {
                    reject(new Error('No se pudo convertir canvas a blob'));
                }
            }, 'image/png', 1.0);
        });

        // Crear nombre de archivo sanitizado
        const sanitizedName = productName
            .trim()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .replace(/[^a-zA-Z0-9\s]+/g, '')
            .replace(/\s+/g, '_')
            .replace(/^_+|_+$/g, '')
            .toLowerCase()
            .substring(0, 40);

        const fileName = `${sanitizedName || 'producto'}.png`;

        // Descargar imagen
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = fileName;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);

        return true;

    } catch (error) {
        let errorMessage = 'Error al descargar código de barras';

        if (error.message.includes('JsBarcode')) {
            errorMessage = 'Librería JsBarcode no disponible';
        } else if (error.message.includes('vacío')) {
            errorMessage = 'El producto no tiene código de barras';
        } else if (error.message.includes('blob')) {
            errorMessage = 'Error al generar la imagen';
        }

        // Si hay una función de notificación disponible, usarla
        if (typeof showNotification !== 'undefined') {
            showNotification(errorMessage, 'error');
        } else {
            alert(errorMessage);
        }

        return false;
    }
}

/**
 * Verifica si el código de barras es válido para el formato CODE128
 * 
 * @param {string} barcodeValue - Código a validar
 * @returns {boolean} true si es válido
 * 
 * @example
 * isValidBarcode('TALLER-00001-FIL'); // true
 * isValidBarcode('');                  // false
 * isValidBarcode('español_ñ');         // false (CODE128 no soporta ñ)
 */
export function isValidBarcode(barcodeValue) {
    if (!barcodeValue || barcodeValue.trim() === '') {
        return false;
    }

    // CODE128 soporta ASCII de 0-127
    // No soporta caracteres especiales como ñ, tildes, etc.
    const validChars = /^[\x00-\x7F]+$/;

    if (!validChars.test(barcodeValue)) {
        return false;
    }

    return true;
}
