# Refactorización: Módulo de Órdenes de Trabajo (Arquitectura Hexagonal)

El módulo de Órdenes representa uno de los **Agregados Complejos (Aggregate Roots)** más críticos del sistema. No se limita a registrar datos, sino que actúa como un nodo central que gestiona transacciones y relaciones con múltiples entidades externas, específicamente Servicios y Empleados, controlando reglas de negocio concurrentes.

## 1. El Rol de la Orden como Agregado Maestro

En lugar de delegar el control relacional a la base de datos a través de operaciones en cascada puras o lógica dispersa en controladores, el diseño táctico sitúa a `OrdenDomain` como el único responsable de admitir o rechazar asociaciones basadas en el estado del negocio.

### Comparativa de Comportamiento Arquitectónico
| Aspecto | Antes (Acoplado) | Ahora (Hexagonal) |
| :--- | :--- | :--- |
| **Validaciones Transversales** | Dispersas en el servicio e instanciadas sobre ORMs de base de datos. | Centralizadas en el dominio encapsulado por los Value Objects (`GarantiaVO`, `EstadoPagoVO`, `PrecioOrdenVO`). |
| **Verificación de Reglas** | Evaluaciones directas sobre atributos físicos (`empleado.estado != "activo"`). | El dominio procesa variables primitivas desacopladas (`asignar_empleado`) para blindar el negocio. |
| **Acoplamiento de Modelos** | Mutación directa de colecciones de SQLAlchemy en las tablas secundarias. | Abstracción total mediante mapeos en listas nativas de dominio traducidas en la capa `Infrastructure`. |

## 2. Organización y Cohesión de Archivos

Cumpliendo rigurosamente con la disposición técnica y las reglas de diseño arquitectónico acordadas, el módulo de órdenes centraliza sus dependencias físicas y lógicas bajo la ruta `src/ordenes/`:

- **Domain Layer (`/domain`):** Hospeda `orden_domain.py`. Lógica pura de Python, aislada por completo de cualquier framework. Controla la validez de precios de servicios y restringe asignaciones a mecánicos inactivos.
- **Application Layer (`/application`):** `orden_service.py` funciona como el director del flujo de trabajo, orquestando repositorios externos y limpiando los patrones de caché reactivos.
- **Infrastructure Layer (`/infrastructure`):**
    - **`schemas/orden_schema.py`**: Modelos estrictos de Pydantic destinados a la capa de presentación y transporte HTTP.
    - **Tablas Intermedias (`orden_servicio.py` / `orden_empleado.py`)**: Estructuras físicas requeridas exclusivamente por el mapeador relacional (SQLAlchemy).
    - **`orden.py` / `orden_repo.py` / `orden_routes.py`**: Adaptadores técnicos encargados de la traducción, persistencia y exposición del recurso.

## 3. Ventajas Estratégicas y de Diseño

1. **Aislamiento Multimodular:** `OrdenDomain` coordina de manera asíncrona la adición de servicios y empleados sin importar si estos datos provienen de una base de datos relacional, un microservicio independiente o un mock en pruebas unitarias.
2. **Encapsulamiento de la Persistencia Relacional:** Las tablas intermedias mapeadas en la infraestructura aíslan por completo al dominio de la complejidad inherente a los cruces de claves primarias (`Many-to-Many`), manteniendo la lista de agregados limpia y orientada a objetos puros.
3. **Consistencia Transaccional:** El servicio asegura que si la validación de un solo ítem (por ejemplo, un mecánico inactivo) falla dentro del dominio puro, ninguna relación se guarda en la base de datos, garantizando atomicidad lógica sin sobrecargar el motor SQL.

---
*Documentación técnica de arquitectura generada tras la migración exitosa del Agregado de Órdenes a Diseño Táctico y Hexagonal.*
