import { fetchFromApi } from "../../data-manager.js";
import { handleApiError } from "../error-handlers.js";
import { showNotification } from "../notification.js";
import { SUPABASE } from "./data-store.js";


/**
 * Sube una imagen a Supabase Storage.
 * @param {File} file - Archivo de imagen a subir
 * @param {string|number} idObject - ID usado para nombrar el archivo
 * @param {string} bucket - Nombre del bucket (por defecto 'productos')
 * @returns {Promise<string>} Nombre del archivo subido (ej: "123.jpg")
 */
export async function uploadImage(file, idObject, bucket = 'productos') {
  if(!file){
    showNotification("No se proporcionó ningun archivo", "info");
  }
  const ext = (file.name.split('.').pop() || '').replace(/[^a-z0-9]/gi, '').toLowerCase();
  const fileName = `${idObject}.${ext}`;

  const { data, error } = await SUPABASE.storage
    .from(bucket)
    .upload(fileName, file, { upsert: true });

  if (error) {
    handleApiError(error);
    throw error;
  }

  return fileName;
}


/**
 * Actualiza la imagen de un producto existente.
 * @param {string|number} idObject - ID del producto
 * @param {File} file - Nueva imagen
 * @param {string} bucket - Bucket de Supabase
 * @param {string} endpoint - Endpoint de la API (ej: 'productos')
 * @returns {Promise<string>} Nombre del archivo actualizado
 */
export async function updateImage(idObject, file, bucket = 'productos', endpoint) {
  if (!file) {
    showNotification('No se proporcionó ningún archivo para actualizar',"info");
  }
  const data = await fetchFromApi(endpoint,idObject);

  if(data.img){
    await deleteImage(data.img,bucket);
  }

  

  const ext = (file.name.split('.').pop() || '').replace(/[^a-z0-9]/gi, '').toLowerCase();
  const fileName = `${idObject}.${ext}`;

  
  const { error } = await SUPABASE.storage
    .from(bucket)
    .upload(fileName, file, { upsert: true });

  if (error) {
    handleApiError(error);
    throw error;
  }

  return fileName;
}

/**
 * Elimina una imagen de Supabase Storage.
 * @param {string} fileName - Nombre del archivo a eliminar (ej: "123.jpg")
 * @param {string} bucket - Bucket de Supabase
 */
export async function deleteImage(fileName, bucket='productos'){
  if (!fileName) return;
  const {error} = await SUPABASE.storage
  .from(bucket)
  .remove([fileName])
  if(error){
    handleApiError(error);
  }
}

/**
 * Obtiene la URL pública de una imagen.
 * @param {string} fileName - Nombre del archivo (ej: "123.jpg")
 * @param {string} bucket - Bucket de Supabase
 * @returns {string} URL pública de la imagen
 */
export function fetchFromImagen(fileName, bucket = 'productos') {
  if(!fileName){
    return;
  }
  const { data } = SUPABASE.storage.from(bucket).getPublicUrl(fileName);
  return data?.publicUrl || '';
}



/**
 * Comprime / redimensiona una imagen File y devuelve un nuevo File (o Blob).
 * @param {File} file - archivo de imagen original
 * @param {Object} options
 *   - maxWidth {number} ancho máximo (px). Default 1200
 *   - maxHeight {number} alto máximo (px). Default 1200
 *   - quality {number} 0..1 para JPEG/WEBP. Default 0.8
 *   - mimeType {string} 'image/jpeg'|'image/webp' etc. Default preserve or 'image/jpeg'
 *   - maxSizeBytes {number} si se alcanza, intenta comprimir; si null siempre intenta
 * @returns {Promise<File>} archivo comprimido
 */
export async function compressImage(file, options = {}) {
  if (!file || !file.type.startsWith('image/')) return file;

  const {
    maxWidth = 1200,
    maxHeight = 1200,
    quality = 0.8,
    mimeType = (file.type === 'image/png' ? 'image/png' : 'image/jpeg'),
    maxSizeBytes = null
  } = options;

  // Si el archivo ya es pequeño y existe un límite, devuelve original
  if (maxSizeBytes && file.size <= maxSizeBytes) return file;

  // Crear bitmap (mejor rendimiento que Image())
  let imgBitmap;
  try {
    imgBitmap = await createImageBitmap(file);
  } catch (err) {
    // fallback a Image() si createImageBitmap no está disponible
    const dataUrl = await new Promise((res, rej) => {
      const fr = new FileReader();
      fr.onload = () => res(fr.result);
      fr.onerror = rej;
      fr.readAsDataURL(file);
    });
    imgBitmap = await new Promise((res, rej) => {
      const img = new Image();
      img.onload = () => {
        // crear canvas y dibujar
        const canvas = document.createElement('canvas');
        canvas.width = img.width;
        canvas.height = img.height;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0);
        canvas.toBlob(blob => {
          createImageBitmap(blob).then(res).catch(rej);
        }, mimeType, quality);
      };
      img.onerror = rej;
      img.src = dataUrl;
    });
  }

  const { width: srcW, height: srcH } = imgBitmap;
  let targetW = srcW;
  let targetH = srcH;

  // calcular escala manteniendo relación de aspecto
  const ratio = Math.min(1, maxWidth / srcW, maxHeight / srcH);
  targetW = Math.round(srcW * ratio);
  targetH = Math.round(srcH * ratio);

  // dibujar en canvas
  const canvas = document.createElement('canvas');
  canvas.width = targetW;
  canvas.height = targetH;
  const ctx = canvas.getContext('2d');

  // opcional: fondo blanco para PNG transparentes si quieres JPG
  if (mimeType === 'image/jpeg') {
    ctx.fillStyle = '#fff';
    ctx.fillRect(0, 0, targetW, targetH);
  }

  ctx.drawImage(imgBitmap, 0, 0, targetW, targetH);

  // convertir a blob con calidad
  const blob = await new Promise((res) => {
    canvas.toBlob((b) => res(b), mimeType, quality);
  });

  // Si se pidió un límite de tamaño y aún lo supera, intentar recortar quality
  if (maxSizeBytes && blob.size > maxSizeBytes) {
    let q = quality;
    let compressed = blob;
    // reducir calidad progresivamente
    while (compressed.size > maxSizeBytes && q > 0.3) {
      q -= 0.1;
      // eslint-disable-next-line no-await-in-loop
      compressed = await new Promise((res) => canvas.toBlob((b) => res(b), mimeType, q));
    }
    // si aún supera, devolver lo mejor que tenemos
    if (compressed) {
      const newFile = new File([compressed], file.name, { type: compressed.type });
      return newFile;
    }
  }

  const newFile = new File([blob], file.name, { type: blob.type });
  return newFile;
}