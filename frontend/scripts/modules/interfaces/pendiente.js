/**
 * Cargar interfaz de Órdenes Pendientes
 * @param {HTMLElement} container - Contenedor donde renderizar
 */
export async function loadPendiente(container) {
  container.innerHTML = `
    <div class="pendiente-container">
      <h2>Órdenes Pendientes</h2>
      <p>Órdenes pendientes...</p>
      <!-- TODO: Implementar lógica de órdenes pendientes -->
    </div>
  `;
}
