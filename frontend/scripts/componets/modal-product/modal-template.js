import { fetchFromApi } from '../../data-manager.js';
import { fetchFromImagen } from '../../utils/store/manager-image.js';
import { CATEGORIAS_PRODUCTOS } from './constants.js';

export function generateCategoryOptions(selectedCategory = '', disabled = false) {
  return CATEGORIAS_PRODUCTOS.map(cat =>
    `<option value="${cat}" ${selectedCategory === cat ? 'selected' : ''} ${disabled ? 'disabled' : ''}>${cat}</option>`
  ).join('');
}

export async function generateModalHTML(type = 'add', id = null) {
  const isEdit = (type === 'edit' && id !== null);
  const isView = (type === 'view' && id !== null);
  const isReadOnly = isView;

  let title = 'Agregar';
  if (isEdit) title = 'Editar';
  if (isView) title = 'Detalles del';

  const required = (isEdit || isView) ? '' : 'required';
  const disabled = isReadOnly ? 'disabled' : '';
  const readonly = isReadOnly ? 'readonly' : '';

  let data = {
    nombre: '',
    marca: '',
    categoria: '',
    stock: '',
    stockMin: '',
    precioCompra: '',
    precioVenta: '',
    descripcion: '',
    modelo: '',
    anio: '',
    img: '',
    tipo: ''
  };

  if (isEdit || isView) {
    data = await fetchFromApi("productos", id);
    if (data.tipo === "autoparte") {
      let autoparte = await fetchFromApi("autopartes", id);
      data.anio = autoparte.anio;
      data.modelo = autoparte.modelo;
    }
  }

  const categoryOptions = generateCategoryOptions(data.categoria, isReadOnly);
  const isAutoparte = data.tipo === 'autoparte' || data.modelo || data.anio;

  return `
  <div class="modal-overlay">
      <div class="modal-inventory-form ${isView ? 'view-mode' : ''}">
          <div class="modal-header">
              ${!isView ? '<button class="modal-info" title="Información" aria-label="Información">&#9432;</button>' : ''}
              <h2 class="form-title">${title} producto</h2>
              <button class="modal-close" title="Cerrar" aria-label="Cerrar">&times;</button>
          </div>
          <form class="form-product" id="form-product" name="form-product">
              <div class="form-group">
                  <label for="product-name" class="form-label">Nombre del producto</label>
                  <input maxlength="50" type="text" id="product-name" name="product-name" 
                         placeholder="${isEdit || isView ? data.nombre : 'Ej: Filtro de aceite'}"
                         value="${data.nombre}" ${required} ${readonly}>
              </div>
              <div class="form-group">
                  <label for="product-brand" class="form-label">Marca</label>
                  <input maxlength="40" type="text" id="product-brand" name="product-brand" 
                         placeholder="${isEdit || isView ? data.marca : 'Ej: Toyota'}"
                         value="${data.marca}" ${readonly}>
              </div>
              <div class="form-group">
                  <label for="product-category" class="form-label">Categoría</label>
                  <select id="product-category" name="product-category" ${required} ${disabled}>
                      <option value="" disabled ${!data.categoria ? 'selected' : ''}>Selecciona una categoría</option>
                      ${categoryOptions}
                  </select>
              </div>
              <div class="form-group">
                  <label for="product-stock" class="form-label">Stock</label>
                  <input type="number" id="product-stock" name="product-stock" 
                         placeholder="${isEdit || isView ? data.stock : 'Ej: 25'}"
                         value="${data.stock}" ${required} min="0" ${readonly}>
              </div>
              <div class="form-group">
                  <label for="product-min-stock" class="form-label">Stock mínimo</label>
                  <input type="number" id="product-min-stock" name="product-min-stock" 
                         placeholder="${isEdit || isView ? data.stockMin : 'Ej: 5'}"
                         value="${data.stockMin}" ${required} min="0" ${readonly}>
              </div>
              <div class="form-group">
                  <label for="product-purchase-price" class="form-label">Precio de compra</label>
                  <input type="number" id="product-purchase-price" name="product-purchase-price" 
                         step="0.01" placeholder="${isEdit || isView ? data.precioCompra : 'Ej: 150.00'}"
                         value="${data.precioCompra}" ${required} min="0" ${readonly}>
              </div>
              <div class="form-group">
                  <label for="product-selling-price" class="form-label">Precio de venta</label>
                  <input type="number" id="product-selling-price" name="product-selling-price" 
                         step="0.01" placeholder="${isEdit || isView ? data.precioVenta : 'Ej: 200.00'}"
                         value="${data.precioVenta}" ${required} min="0" ${readonly}>
              </div>

              <div class="form-group">
                  <label for="product-description" class="form-label">Descripción</label>
                  <textarea maxlength="500" id="product-description" name="product-description" 
                            placeholder="${isEdit || isView ? data.descripcion : 'Descripción del producto...'}" ${readonly}>${data.descripcion}</textarea>
              </div>
              ${!isView ? `
              <div class="autopart-toggle">
                  <label class="autopart-toggle-label">
                      <input type="checkbox" id="product-autopart" ${isAutoparte ? 'checked' : ''} ${isEdit && isAutoparte ? 'disabled' : ''}>
                      <span>Producto Autoparte</span>
                  </label>
              </div>
              ` : (isAutoparte ? '<div class="autopart-badge"><span>✓ Producto Autoparte</span></div>' : '')}
              
              <div class="auto-part-fields ${isAutoparte ? 'is-visible' : ''}" data-autopart-fields>
                  <div class="form-group">
                      <label for="product-model" class="form-label">Modelo compatible</label>
                      <input maxlength="100" type="text" id="product-model" name="product-model" 
                             placeholder="${isEdit || isView ? data.modelo : 'Ej: Toyota Corolla'}"
                             value="${data.modelo || ''}" ${readonly}>
                  </div>
                  <div class="form-group">
                      <label for="product-year" class="form-label">Año compatible</label>
                      <input maxlength="40" type="text" id="product-year" name="product-year" 
                             placeholder="${isEdit || isView ? data.anio : 'Ej: 2022, 2023'}"
                             value="${data.anio || ''}" ${readonly}>
                  </div>
              </div>
              
              <div class="form-img">
                <label class="form-label">Imagen del producto</label>
                ${!isView ? `
                <div class="image-upload-wrapper">
                    <label class="custom-file-upload">
                        <input type="file" id="product-img" name="product-img" accept="image/jpeg, image/jpg, image/png, image/webp">
                        Seleccionar imagen
                    </label>
                    <span class="file-name" id="file-name">Ningún archivo seleccionado</span>
                </div>
                ` : ''}
                ${(isEdit || isView) && data.img ?
      `<img id="product-preview" class="product-preview show" alt="Vista previa" src="${fetchFromImagen(data.img, 'productos')}" style="display:block;max-width:100%;height:auto;border-radius:8px;margin-top:12px;">` :
      `<img id="product-preview" class="product-preview" alt="Vista previa" style="display:none">`
    }
                ${!isView ? `
                <div class="image-info">
                    <span>Formatos permitidos: JPG, PNG, WEBP</span>
                    <span>Tamaño máximo: 20 MB</span>
                </div>
                ` : ''}
              </div>
              
              <! -- Código de barras -->
              ${(isEdit || isView) && data.codBarras ? `
              <div class="form-group barcode-group">
                  <label class="form-label">Código de barras</label>
                  <div class="barcode-container" id="barcode-container" 
                       title="Haz clic para descargar la imagen"
                       style="cursor: pointer; padding: 4px; border: 1px solid #ddd; border-radius: 8px; background: #fff; display: flex; align-items: center; justify-content: center; gap: 15px;">
                      <svg id="product-barcode"></svg>
                      <p style="margin: 0; font-size: 12px; color: #3498db; font-weight: 500; white-space: nowrap;">
                        Haz clic para<br>descargar
                      </p>
                  </div>
              </div>
              ` : ''}

              <div class="form-actions">
                  ${!isView ? `
                  <button type="submit" class="btn-save">${isEdit ? 'Actualizar' : 'Guardar'}</button>
                  <button type="button" class="btn-cancel">Cancelar</button>
                  ` : `
                  <button type="button" class="btn-cancel">Cerrar</button>
                  `}
              </div>
          </form>
      </div>
  </div>
    `;
}