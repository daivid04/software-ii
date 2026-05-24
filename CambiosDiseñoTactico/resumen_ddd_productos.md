# Resumen de Refactorización: Del CRUD Anémico a DDD Táctico

Este documento resume brevemente los cambios estratégicos realizados en el módulo de **Productos** para migrar de una arquitectura CRUD tradicional hacia un **Diseño Táctico con Domain-Driven Design (DDD)**, erradicando la anemia del dominio y protegiendo las reglas del negocio.

---

## 📊 Comparativa General

| Característica | Antes (Modelo Anémico) | Ahora (Modelo Rico - DDD) |
| :--- | :--- | :--- |
| **Ubicación de la Lógica** | Secuestrada en los servicios (`producto_service.py`) y alterada directamente desde afuera. | Centralizada dentro de la propia Entidad (`producto.py`). |
| **Modificación de Datos** | Abierta mediante manipulación directa de atributos o bucles genéricos `setattr`. | Encapsulada mediante métodos explícitos del negocio (**Lenguaje Ubicuo**). |
| **Validaciones de Negocio** | Dispersas en el servicio o delegadas únicamente a la validación de entrada de Pydantic. | Inmediatas y autovalidadas por los **Value Objects** inmutables. |
| **Rol del Repositorio** | Modificaba estados de los objetos de base de datos de manera arbitraria. | Actúa únicamente como mecanismo de persistencia para el **Aggregate Root** (`guardar`). |

---

## 🛠️ Resumen de Cambios por Archivo

### 1. `db/models/value_objects.py` *(Nuevo Archivo)*
* Se crearon las clases inmutables (`@dataclass(frozen=True)`) **PrecioVO** e **InventarioVO**.
* Contienen las reglas críticas del negocio (por ejemplo, que los precios o el stock nunca sean negativos, y que el precio de venta supere al de compra) aisladas de cualquier framework.

### 2. `db/models/producto.py` *(Aggregate Root)*
* Dejó de ser un contenedor pasivo de datos para convertirse en la **Raíz del Agregado**.
* Se agregaron métodos de dominio ricos: `actualizar_informacion_basica()`, `establecer_precios()` y `ajustar_inventario()`.

### 3. `repositories/producto_repo.py` *(Persistencia Estricta)*
* Se eliminó el bucle anémico que iteraba con `setattr`.
* Se implementó el método `guardar(producto)` que recibe la entidad previamente validada por el dominio y simplemente la persiste en la base de datos.

### 4. `services/producto_service.py` *(Capa de Aplicación)*
* Ya no toma decisiones de negocio de forma externa ni altera campos individuales.
* Actúa como coordinador: recupera la entidad, invoca sus métodos ricos de negocio y delega al repositorio guardar los cambios.

### 5. `api/v1/routes/producto_routes.py` *(Controlador / API)*
* Mantiene exactamente las mismas rutas y estructura consumidas por el frontend.
* Se añadieron bloques `try...except ValueError` en los endpoints de mutación (`POST` y `PUT`) para capturar fallos de los Value Objects y traducirlos limpiamente en errores `400 Bad Request`.
