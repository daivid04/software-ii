import { showWarning } from '../utils/notification.js';
import { fetchProductoByBarCode } from '../services/venta-api.js';
import { escapeHtml } from '../utils/sanitize.js';

let barcodeBuffer = "";
let lastBarcodeTime = 0;

/**
 * Inicializar lector de códigos de barras
 * Detecta escaneos por velocidad de escritura
 */
export function initBarcodeReader() {
  document.addEventListener("keydown", async (event) => {
    const reader = document.getElementById('producto-search');
    if (!reader) return;

    const currentTime = Date.now();
    const timeDiff = currentTime - lastBarcodeTime;
    lastBarcodeTime = currentTime;

    // Si es Enter, procesar código escaneado
    if (event.key === "Enter") {
      if (barcodeBuffer.length > 2) {
        event.preventDefault();
        const barCode = barcodeBuffer.replaceAll("'", "-");
        await processScannedProduct(barCode, reader);
        barcodeBuffer = "";
      } else {
        barcodeBuffer = "";
      }
      return;
    }

    // Ignorar teclas especiales
    if (event.key.length > 1) return;

    // Detectar escaneo por velocidad (< 60ms entre teclas)
    if (timeDiff < 60) {
      event.preventDefault();

      // Corregir primer carácter si se escribió en input
      if (barcodeBuffer.length === 1 && document.activeElement.tagName === 'INPUT') {
        const input = document.activeElement;
        if (input.value.endsWith(barcodeBuffer)) {
          input.value = input.value.slice(0, -1);
        }
      }

      barcodeBuffer += event.key;
    } else {
      barcodeBuffer = event.key;
    }
  });
}

/**
 * Procesar producto escaneado
 * @param {string} barCode - Código de barras
 * @param {HTMLElement} reader - Input donde mostrar resultado
 */
async function processScannedProduct(barCode, reader) {
  const { showSuccess, showError } = await import('../utils/notification.js');
  
  try {
    const producto = await fetchProductoByBarCode(barCode);

    if (!producto) {
      showWarning(`Producto no encontrado: ${barCode}`);
      return;
    }

    if (producto.stock === 0) {
      showWarning(`Sin stock: ${producto.nombre}`);
      return;
    }

    // Llenar datos del producto
    reader.value = producto.nombre;
    reader.dataset.selectedId = producto.id;
    reader.dataset.precio = producto.precio_venta;
    reader.dataset.stock = producto.stock;

    // Cerrar dropdown
    const dropdown = document.getElementById('producto-dropdown');
    if (dropdown) dropdown.style.display = 'none';

    showSuccess(`Producto detectado: ${producto.nombre}`);

    // Mover foco a cantidad
    const cantidadInput = document.getElementById('cantidad-input');
    if (cantidadInput) {
      cantidadInput.value = 1;
      cantidadInput.focus();
      cantidadInput.select();
    }

  } catch (error) {
    showError('Error al procesar código de barras');
  }
}

/**
 * Resetear buffer del barcode
 */
export function resetBarcodeBuffer() {
  barcodeBuffer = "";
  lastBarcodeTime = 0;
}
