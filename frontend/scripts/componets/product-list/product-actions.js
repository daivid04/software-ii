import { openModalForm } from '../modal-product/modal-product.js';
import { deleteResource, fetchFromApi } from '../../data-manager.js';
import { showNotification } from '../../utils/notification.js';
import { confirmDelete } from '../modal-confirm.js';
import { deleteImage } from '../../utils/store/manager-image.js';
import { renderProducts } from './product-list.js';

// Variable para evitar múltiples listeners
let isListenerAttached = false;

export function setupProductActions() {
  if (isListenerAttached) return;
  
  const productList = document.getElementById("product-list");
  if (!productList) return;
  
  // Delegar eventos una sola vez
  productList.addEventListener('click', async (e) => {
    const target = e.target;
    
    // Click en el producto para ver detalles
    const productItem = target.closest('.product-item');
    if (productItem && !target.closest('.product-actions-product')) {
      const idStr = productItem.getAttribute("data-product-id");
      const idProduct = parseInt(idStr);
      openModalForm('view', idProduct);
      return;
    }
    
    // Click en botones de acción
    const actionButton = target.closest('.product-actions-product');
    if (actionButton) {
      e.stopPropagation();
      
      const idStr = actionButton.getAttribute("data-id");
      const idProduct = parseInt(idStr);
      const action = actionButton.dataset.action;
      
      if (action === 'edit') {
        openModalForm('edit', idProduct);
      } else if (action === 'delete') {
        await handleDeleteProduct(idProduct);
      }
    }
  });
  
  isListenerAttached = true;
}

export function setupViewProduct() {
  // Ya no se necesita, todo se maneja en setupProductActions con delegación
}

async function handleDeleteProduct(productId) {
  const confirmed = await confirmDelete(productId);
  
  if (!confirmed) return;
  
  try {
    const product = await fetchFromApi('productos', productId, true);
    
    // Si el producto no existe (puede haber sido eliminado previamente)
    if (!product) {
      showNotification('El producto ya no existe', 'warning');
      // Obtener lista actualizada y re-renderizar
      const updatedProducts = await fetchFromApi('productos', null, true);
      await renderProducts(updatedProducts);
      window.dispatchEvent(new CustomEvent('inventory:products-updated', {
        detail: updatedProducts,
      }));
      return;
    }
    
    await deleteResource('productos', productId);

    if (product?.img) {
      await deleteImage(product.img,'productos');
    }
    
    // Obtener lista fresca del servidor
    const updatedProducts = await fetchFromApi('productos', null, true);
    
    // Actualizar la lista de productos
    await renderProducts(updatedProducts);
    
    // Disparar evento DESPUÉS de renderizar para que filtros se actualicen
    window.dispatchEvent(new CustomEvent('inventory:products-updated', {
      detail: updatedProducts,
    }));
    
    showNotification('Producto eliminado exitosamente', 'success');
    
  } catch (error) {
    
    // Si es un 404, significa que ya fue eliminado
    if (error.status === 404) {
      showNotification('El producto ya fue eliminado', 'warning');
      // Refrescar la lista para que desaparezca de la UI
      const updatedProducts = await fetchFromApi('productos', null, true);
      await renderProducts(updatedProducts);
      window.dispatchEvent(new CustomEvent('inventory:products-updated', {
        detail: updatedProducts,
      }));
    } else {
      showNotification('Error al eliminar producto', 'error');
    }
  }
}