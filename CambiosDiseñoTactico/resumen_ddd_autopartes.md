# Resumen de Refactorización: Módulo de Autopartes a DDD Táctico

Este documento resume brevemente los cambios estratégicos realizados en el módulo de **Autopartes** para migrar de una arquitectura CRUD tradicional hacia un **Diseño Táctico con Domain-Driven Design (DDD)**, especializando la entidad como raíz de agregado y protegiendo sus reglas de compatibilidad.

---

## 📊 Comparativa General

| Característica | Antes (Modelo Anémico) | Ahora (Modelo Rico - DDD) |
| :--- | :--- | :--- |
| **Ubicación de la Lógica** | Secuestrada en los servicios (`autoparte_service.py`) y alterada directamente desde afuera. | Centralizada en la Entidad especializada (`autoparte.py`) heredando comportamiento base. |
| **Modificación de Datos** | Abierta mediante manipulación directa de atributos o bucles genéricos `setattr` en el repositorio. | Encapsulada mediante métodos explícitos del negocio (**Lenguaje Ubicuo**). |
| **Validaciones de Negocio** | Dispersas o inexistentes para campos específicos como modelo y año del vehículo. | Inmediatas y autovalidadas por el nuevo **Value Object** inmutable. |
| **Rol del Repositorio** | Forzaba mapeos e inserciones directas alterando columnas arbitrariamente. | Actúa únicamente como mecanismo de persistencia para el **Aggregate Root** (`guardar`). |

---

## 🛠️ Resumen de Cambios por Archivo

### 1. `db/models/value_objects.py` *(Actualización)*
* Se añadió la clase inmutable (`@dataclass(frozen=True)`) **CompatibilidadVehiculoVO**.
* Valida automáticamente que las especificaciones del modelo y el rango/formato del año del vehículo tengan coherencia comercial antes de guardarse.

### 2. `db/models/autoparte.py` *(Aggregate Root Especializado)*
* Al heredar de `Producto`, mantiene el control total de precios e inventario base.
* Se agregó el método de dominio enriquecido `asignar_compatibilidad()` para manejar sus propios atributos sin permitir setters públicos.

### 3. `repositories/autoparte_repo.py` *(Persistencia Estricta)*
* Se eliminó el bucle anémico basado en `setattr` dentro de la actualización.
* Se implementó el método `guardar(autoparte)` encargado únicamente de sincronizar el estado validado de la entidad con la base de datos de Supabase.

### 4. `services/autoparte_service.py` *(Capa de Aplicación)*
* Se eliminó el flujo que enviaba datos sueltos al repositorio.
* Ahora actúa como intermediario puro: obtiene la entidad, invoca los comportamientos ricos del dominio (`actualizar_informacion_basica`, `establecer_precios`, `ajustar_inventario`, `asignar_compatibilidad`) y solicita al repositorio persistir los cambios.

### 5. `api/v1/routes/autoparte_routes.py` *(Controlador / API)*
* Mantiene estables todos los endpoints consumidos originalmente por el frontend.
* Se envolvieron las peticiones de mutación (`POST` y `PUT`) en bloques `try...except ValueError` para enviar respuestas `400 Bad Request` en caso de violaciones del dominio, y un manejo preventivo de `Exception` para conflictos en el `DELETE`.
