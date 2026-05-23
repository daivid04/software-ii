/**
 * Cargar interfaz de Historial de Servicios
 * @param {HTMLElement} container - Contenedor donde renderizar
 */
export async function loadHistorialServicios(container) {
  container.innerHTML = `
    <div class="historial-container">
      <h2>Historial de Servicios</h2>
      <p>Ver historial de servicios...</p>
      <!-- TODO: Implementar lógica de historial -->
    </div>
  `;
}
