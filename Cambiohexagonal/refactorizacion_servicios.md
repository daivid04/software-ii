# Refactorización: Módulo de Servicios (Arquitectura Hexagonal)

Se ha migrado el módulo de Servicios siguiendo los principios de Arquitectura Hexagonal y Domain-Driven Design (DDD), garantizando el aislamiento completo de las reglas de negocio frente a los mecanismos de persistencia.

## 1. Desacoplamiento de la Lógica de Negocio

Anteriormente, el modelo de base de datos (`Servicio`) contenía directamente el método de mutación y validación de estado. Con la nueva estructura, la infraestructura se vuelve totalmente pasiva y delegada, mientras que el Dominio asume la inteligencia.

### Comparativa de Responsabilidades
| Componente | Antes (Acoplado) | Ahora (Hexagonal) |
| :--- | :--- | :--- |
| **Entidad de Negocio** | Clase ORM de SQLAlchemy (`Servicio`). | `ServicioDomain` (Clase pura de Python). |
| **Validación de Datos** | Delegada directamente en el modelo ORM. | Centralizada en `ServicioDomain` mediante `InformacionServicioVO`. |
| **Flujo de Modificación** | Modificación directa sobre las columnas del ORM. | Ciclo de conversión: `ORM -> Dominio -> Lógica -> ORM`. |
| **Persistencia** | Acoplada al modelo y repositorios mixtos. | `ServicioRepository` enfocado en operaciones puras de base de datos. |

## 2. Nueva Estructura del Módulo

El código se ha organizado de forma estricta en tres capas conceptuales dentro de `src/servicios/`:

- **Capa de Dominio (`/domain`):** Contiene `ServicioDomain`. Es una estructura ligera que procesa los cambios de nombre y descripción, autoprotegiéndose de entradas inválidas o inyecciones maliciosas mediante el uso de Value Objects compartidos (`InformacionServicioVO`).
- **Capa de Aplicación (`/application`):** `ServicioService` actúa como el único orquestador del flujo de trabajo, gestionando además las estrategias de invalidación y lectura de caché de forma limpia.
- **Capa de Infraestructura (`/infrastructure`):** Aloja el mapeo físico de SQLAlchemy (`Servicio`), los adaptadores de persistencia (`ServicioRepository`) y los puntos de entrada HTTP (`ServicioRoutes`).

## 3. Beneficios Técnicos Alcanzados

1. **Aislamiento Arquitectónico:** El núcleo de la lógica de servicios ya no depende de las decisiones técnicas de almacenamiento (SQLAlchemy, PostgreSQL, etc.).
2. **Coherencia del Sistema:** Al adoptar la secuencia de transformación `to_domain()` y `from_domain()`, el módulo mantiene el mismo diseño táctico implementado con éxito en *Productos*, *Autopartes* y *Ventas*.
3. **Optimización del Estado (Caché):** Se preserva el comportamiento del decorador de caché en la capa de aplicación, asegurando la consistencia de los datos en memoria ante registros, actualizaciones o bajas del catálogo.

---
*Documentación de la arquitectura del software generada tras concluir la migración del catálogo de servicios.*
