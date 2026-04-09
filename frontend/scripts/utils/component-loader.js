/**
 * Carga un componente HTML en un elemento destino si está vacío.
 * Esto permite compatibilidad híbrida:
 * - VPS (Nginx SSI): El contenido ya estará presente, no hace nada.
 * - Local (Python): El contenido estará vacío (solo comentarios), carga el HTML.
 * 
 * @param {string} elementId - ID del elemento donde se inyectará el HTML.
 * @param {string} path - Ruta al archivo HTML del componente.
 */
export async function loadComponent(elementId, path) {
  try {
    const element = document.getElementById(elementId);
    if (!element) {
      // Elemento no existe en esta página, ignorar
      return;
    }

    // Verificar si ya tiene contenido (ignora espacios en blanco y comentarios)
    const content = element.innerHTML.replace(/<!--[\s\S]*?-->/g, '').trim();

    if (content.length > 0) {
      // Ya tiene contenido (probablemente cargado por SSI), no hacer nada
      return;
    }

    // Si está vacío, cargar dinámicamente
    const response = await fetch(path);
    if (!response.ok) {
      throw new Error(`Error cargando ${path}: ${response.statusText}`);
    }

    const html = await response.text();
    element.innerHTML = html;

  } catch (error) {
    const element = document.getElementById(elementId);
    if (element) {
      element.innerHTML = `<p style="color:red">Error cargando componente</p>`;
    }
  }
}
