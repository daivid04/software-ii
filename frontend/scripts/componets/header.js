/**
 * Carga y retorna el HTML del encabezado (header)
 * Muestra el logo y nombre del taller en la parte superior
 * @param {*} param - Parámetro opcional (no utilizado actualmente)
 * @returns {string} HTML del header con logo y título
 */
export function loadHeader(param) {
    return `
        <div class="header-container">
          <div class="header-name">
            <!-- Logo del taller -->
            <img src="../assets/images/logo.svg" alt="Logo Taller Diego" class="logo">
            
            <!-- Nombre del taller -->
            <h1>Taller de Diego</h1>
          </div>
          <div class="header-close" id="logout-btn">
              <img src="../assets/icons/salida.png" alt="Logo de cerrar sesión">
          </div>
      </div>
      <script type="module" src="../scripts/header-actions.js"></script>
    `;
}