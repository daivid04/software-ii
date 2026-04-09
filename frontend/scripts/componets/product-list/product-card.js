import { escapeHtml } from '../../utils/sanitize.js';

function formatCurrency(value) {
  const amount = Number(value);
  if (Number.isNaN(amount)) {
    return '$0';
  }
  return new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    maximumFractionDigits: 0,
  }).format(amount);
}

export function generateProductCard(product) {
  const stock = Number(product?.stock ?? 0);
  const stockMin = Number(product?.stockMin ?? 0);
  const classStock = `product-stock ${stockMin > stock ? 'low-stock' : 'normal-stock'}`;

  const safeName = escapeHtml(product?.nombre);
  const safeDescription = escapeHtml(product?.descripcion || 'Sin descripción');
  const safePurchasePrice = formatCurrency(product?.precioCompra);
  const safeSellingPrice = formatCurrency(product?.precioVenta);

  return `
  <div class="product-item" data-product-id="${escapeHtml(product?.id)}">
    <div class="product-name">${safeName}</div>
    <div class="product-desc">${safeDescription}</div>
    <div class="${classStock}">${escapeHtml(stock)}</div>
    <div class="product-purchase-price">${safePurchasePrice}</div>
    <div class="product-selling-price">${safeSellingPrice}</div>
    <div class="product-actions">
      <button class="btn-edit product-actions-product" data-id="${escapeHtml(product?.id)}" data-action="edit">
        <img class="img-edit" src="../assets/icons/edit.png" alt="Editar">
      </button>
      <button class="btn-delete product-actions-product" data-id="${escapeHtml(product?.id)}" data-action="delete">
        <img class="img-delete" src="../assets/icons/delete.png" alt="Eliminar">
      </button>
    </div>
  </div>`;
}