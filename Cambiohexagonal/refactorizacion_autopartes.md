# Refactorización: Módulo de Autopartes (Hexagonal)

Se ha migrado el módulo de Autopartes siguiendo los principios de Arquitectura Hexagonal y Domain-Driven Design (DDD), logrando un desacoplamiento total entre la lógica de negocio y la persistencia de datos.

## 1. Cambio de Paradigma: Dependencia Invertida

Hemos pasado de una estructura donde la base de datos dictaba el comportamiento, a una donde el Dominio es el núcleo del sistema.

### Comparativa de Dependencias
| Aspecto | Antes (Acoplado) | Ahora (Hexagonal) |
| :--- | :--- | :--- |
| **Entidad** | Clase SQLAlchemy (ORM). | `AutoparteDomain` (Clase Pura). |
| **Lógica** | Dentro de la clase ORM. | Centralizada en `AutoparteDomain`. |
| **Persistencia** | El Servicio llamaba al ORM. | El Servicio orquesta el Dominio y Repositorio. |
| **Herencia** | Herencia de tabla SQLAlchemy. | Herencia de Dominio + Herencia de Tabla. |

## 2. Estructura de Capas
El módulo ahora se organiza por responsabilidad:

- **Dominio (`/domain`):** Lógica pura. `AutoparteDomain` hereda de `ProductoDomain` y gestiona las reglas de compatibilidad (modelo/año) sin saber que existe SQLAlchemy.
- **Aplicación (`/application`):** El `AutoparteService` actúa como orquestador.
- **Infraestructura (`/infrastructure`):** `Autoparte` (ORM) y `AutoparteRepository`. Implementan los mapeadores `to_domain` y `from_domain` para comunicarse con la base de datos.

## 3. Beneficios Clave
1. **Polimorfismo controlado:** Se mantiene la herencia de SQLAlchemy (`__mapper_args__`) para la base de datos, pero se desacopla la lógica mediante el patrón de puente (`to_domain`/`from_domain`).
2. **Reutilización:** `AutoparteDomain` aprovecha toda la lógica de negocio ya definida en `ProductoDomain`, evitando la duplicación de código.
3. **Mantenibilidad:** Cualquier cambio en la validación de compatibilidad o precios se hace exclusivamente en el Dominio, sin afectar la capa de base de datos.
4. **Testabilidad:** Ahora es posible realizar tests unitarios de las reglas de negocio de `Autoparte` sin necesidad de levantar una conexión a base de datos.

---
*Documentación generada automáticamente como parte de la refactorización a Arquitectura Hexagonal.*
