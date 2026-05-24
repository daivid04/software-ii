# Resumen de Refactorización: Módulo de Ventas a DDD Táctico

Este documento resume brevemente los cambios estratégicos realizados en el módulo de **Ventas** para migrar de una arquitectura CRUD tradicional hacia un **Diseño Táctico con Domain-Driven Design (DDD)**, centralizando el control operacional e inventario en la raíz agregada.

---

## 📊 Comparativa General

| Característica | Antes (Modelo Anémico) | Ahora (Modelo Rico - DDD) |
| :--- | :--- | :--- |
| **Ubicación de la Lógica** | Secuestrada en el repositorio (`venta_repo.py`), restando stock y enlazando entidades de forma anémica. | Centralizada en el Aggregate Root (`venta.py`) orquestando sus entidades internas de forma íntegra. |
| **Modificación de Datos** | El repositorio alteraba directamente las propiedades del producto y creaba registros huérfanos. | Encapsulada mediante métodos explícitos del negocio (**Lenguaje Ubicuo**). |
| **Validaciones de Negocio** | Delegadas a flujos lineales e imperativos propensos a datos corruptos. | Inmediatas y autovalidadas en la raíz mediante los nuevos **Value Objects** inmutables. |
| **Tablas Intermedias** | Tratadas como entidades independientes manejadas desde repositorios genéricos. | Gobernadas estricta y exclusivamente por la Raíz del Agregado (`VentaProducto`). |

---

## 🛠️ Resumen de Cambios por Archivo

### 1. `db/models/value_objects.py` *(Actualización)*
* Se añadieron las clases inmutables (`@dataclass(frozen=True)`) **CantidadVentaVO** y **FechaVentaVO**.
* Regulan de forma estricta que las cantidades facturadas sean mayores a cero y que el registro histórico de transacciones del taller no admita fechas del futuro.

### 2. `db/models/venta.py` *(Aggregate Root)*
* Se transformó en el **Aggregate Root** absoluto del proceso de facturación.
* Se incorporaron los métodos ricos `inicializar_fecha()` y `agregar_detalle()`, este último interactuando con la raíz del agregado `Producto` (`registrar_despacho`) para asegurar la consistencia del stock.

### 3. `repositories/venta_repo.py` *(Persistencia Estricta)*
* Se eliminó por completo el método `registrar_venta_con_productos` que secuestraba la matemática comercial y de inventario.
* Se implementó el método unificado `guardar(venta)`, cuya única responsabilidad técnica es persistir el estado cohesivo del agregado completo en Supabase.

### 4. `services/venta_service.py` *(Capa de Aplicación)*
* Ya no delega mapeos estructurados ni lógica procedimental cruda al repositorio.
* Actúa como coordinador puro: localiza las raíces afectadas, delega las acciones imperativas del dominio a la entidad `Venta` e indica al repositorio guardar los cambios resultantes.

### 5. `api/v1/routes/venta_routes.py` *(Controlador / API)*
* Preserva estables todos los endpoints originales consumidos por el cliente del taller.
* Centraliza las capturas controladas de fallas de negocio en el servicio, transformando los `ValueError` del dominio directamente en respuestas estandarizadas `400 Bad Request`.
