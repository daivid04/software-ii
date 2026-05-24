# Refactorización: Módulo de Productos (Arquitectura Hexagonal)

El módulo de Productos constituye el "Núcleo" (Core) de nuestro sistema de inventario. Su refactorización a Arquitectura Hexagonal ha sido fundamental para permitir la extensión mediante especializaciones como `Autopartes`.

## 1. De Entidad a Dominio: El Cambio Fundamental

Anteriormente, nuestra clase `Producto` estaba fuertemente acoplada a SQLAlchemy. Ahora, hemos separado la lógica de negocio (dominio) de la persistencia (infraestructura).

### Comparativa de Estructura
| Aspecto | Antes (Acoplado) | Ahora (Hexagonal) |
| :--- | :--- | :--- |
| **Entidad** | Clase SQLAlchemy (ORM). | `ProductoDomain` (Dataclass). |
| **Lógica** | Métodos mezclados con ORM. | Métodos puros en `ProductoDomain`. |
| **Persistencia** | SQL en la misma clase. | Capa `Infrastructure` (Repository). |
| **Mapeo** | N/A (Directo). | `to_domain` y `from_domain` (Bridges). |

## 2. Componentes Principales

- **Domain Layer (`producto_domain.py`):**
    - Definida como una `@dataclass`.
    - Contiene la lógica de negocio "pura": cálculo de precios, validación de stock y reglas de negocio transversales.
    - No conoce nada sobre la base de datos o FastAPI.

- **Infrastructure Layer (`producto.py`):**
    - Clase ORM de SQLAlchemy.
    - Define la estructura de la tabla `productos`.
    - Implementa `to_domain()` para convertir el registro de BD a un objeto de Dominio.
    - Implementa `from_domain()` para actualizar el registro de BD con los cambios del Dominio.

## 3. Beneficios Estratégicos

1. **Polimorfismo:** Gracias a la configuración `__mapper_args__` de SQLAlchemy, `Producto` actúa como la base para especializaciones (`Autopartes`, etc.), permitiendo que el repositorio trate a todos como `Producto` para operaciones generales, pero manteniendo la estructura física correcta.
2. **Encapsulamiento:** La lógica de "aumentar stock" o "cambiar precio" solo puede ser invocada a través de los métodos del Dominio (`establecer_precios`, `ajustar_inventario`), protegiendo la integridad de los datos.
3. **Desacoplamiento:** Ahora podemos cambiar nuestra estrategia de persistencia (ej. migrar de PostgreSQL a otra base de datos o usar archivos planos) sin tocar una sola línea de lógica de negocio en `ProductoDomain`.

---
*Este módulo ahora sirve como la base sólida sobre la cual escalaremos el resto de los catálogos del sistema.*
