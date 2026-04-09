/**
 * Carga y retorna el HTML del menú lateral (sidebar)
 * Este componente muestra la navegación principal de la aplicación
 * @returns {string} HTML del sidebar con todos los enlaces de navegación
 */
export function loadSideBar() {
    return `
        <nav class="sidebar-nav">
            <ul>
                <!-- Opción de navegación: Inicio/Dashboard -->
                <li>
                    <a href="index.html">
                        <img src="../assets/icons/home.png" alt="Home" class="icon">
                        <span>Inicio</span>
                    </a>
                </li>
                
                <!-- Opción de navegación: Inventario -->
                <li>
                    <a href="inventory.html">
                        <img src="../assets/icons/package.png" alt="Inventario" class="icon">
                        <span>Inventario</span>
                    </a>
                </li>
                
                <!-- Opción de navegación: Servicios -->
                <li>
                    <a href="service.html">
                        <img src="../assets/icons/toolbox.png" alt="Servicios" class="icon">
                        <span>Servicios</span>
                    </a>
                </li>
                
                <!-- Opción de navegación: Órdenes de servicio -->
                <li>
                    <a href="orden.html">
                        <img src="../assets/icons/checklist.png" alt="Orden de servicio" class="icon">
                        <span>Orden</span>
                    </a>
                </li>
                
                <!-- Opción de navegación: Personal -->
                <li>
                    <a href="#">
                        <img src="../assets/icons/leader.png" alt="Personal" class="icon">
                        <span>Personal</span>
                    </a>
                </li>
            </ul>
        </nav>
    `;
}