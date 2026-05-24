# Resumen de Refactorización: Módulo de Órdenes de Trabajo a DDD Táctico

Este documento resume brevemente los cambios estratégicos realizados en el módulo de **Órdenes de Trabajo** para migrar de una arquitectura CRUD tradicional hacia un **Diseño Táctico con Domain-Driven Design (DDD)**, estructurando la entidad como el orquestador central de servicios y empleados del taller.

---

## 📊 Comparativa General

| Característica | Antes (Modelo Anémico) | Ahora (Modelo Rico - DDD) |
| :--- | :--- | :--- |
| **Ubicación de la Lógica** | Dispersa en el repositorio (`orden_repo.py`), enlazando relaciones de forma lineal y desprotegida. | Centralizada en el Aggregate Root (`orden.py`), gobernando sus propias entidades internas. |
| **Modificación de Datos** | El repositorio alteraba e insertaba directamente registros en las tablas intermedias de forma anémica. | Encapsulada mediante métodos explícitos del negocio (**Lenguaje Ubicuo**). |
| **Validaciones de Negocio** | Ausentes o delegadas a flujos procedimentales externos. | Inmediatas y autovalidadas por los nuevos **Value Objects** inmutables. |
| **Tablas Intermedias** | Mapeadas y manipuladas directamente desde el repositorio de forma desarticulada. | Gobernadas estricta y exclusivamente por la Raíz del Agregado (`OrdenServicio` y `OrdenEmpleado`). |

---

## 🛠️ Resumen de Cambios por Archivo

### 1. `db/models/value_objects.py` *(Actualización)*
* Se añadieron las clases inmutables (`@dataclass(frozen=True)`) **GarantiaVO**, **EstadoPagoVO** y **PrecioOrdenVO**.
* Regulan que los días de garantía y precios cobrados no sean negativos, y restringen el estado de pago a opciones comerciales válidas (`pendiente`, `pagado`, `parcial`, `cancelado`).

### 2. `db/models/orden.py` *(Aggregate Root)*
* Se transformó en el **Aggregate Root** encargado de centralizar las operaciones del taller.
* Se incorporaron los métodos ricos `inicializar_datos_basicos()`, `agregar_servicio()` y `asignar_empleado()`, este último validando que el mecánico se encuentre activo antes de la asignación.

### 3. `repositories/orden_repo.py` *(Persistencia Estricta)*
* Se eliminaron por completo las funciones procedimentales complejas de mapeo manual (`registrar_orden_con_servicios`).
* Se implementó el método unificado `guardar(orden)`, que de forma atómica y limpia persiste todo el árbol de la orden (con sus servicios y empleados asociados) en Supabase.

### 4. `services/orden_service.py` *(Capa de Aplicación)*
* Se removió la lógica de conversión estructural de datos hacia diccionarios crudos.
* Actúa como coordinador puro: inyecta dependencias para buscar entidades asociadas, delega las acciones operativas a la raíz del agregado `Orden` y solicita al repositorio guardar los cambios resultantes.

### 5. `api/v1/routes/orden_routes.py` *(Controlador / API)*
* Preserva estables todos los endpoints originales consumidos por el cliente del taller.
* Captura fallos de integridad referencial convirtiendo las excepciones correspondientes en respuestas estandarizadas `409 Conflict`.
