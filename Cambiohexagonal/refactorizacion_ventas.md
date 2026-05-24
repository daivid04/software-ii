# Refactorización: Módulo de Ventas (Arquitectura Hexagonal)

El módulo de Ventas es uno de los más complejos porque actúa como un **Agregado (Aggregate Root)**. Una Venta no existe de forma aislada; contiene Detalles de Venta y coordina actualizaciones de inventario con los Productos.

## 1. El Concepto de Agregado en DDD

En lugar de tratar la Venta y sus Detalles como tablas sueltas de base de datos, ahora tratamos a la Venta como una única unidad lógica.

### Comparativa de Estructura
| Aspecto | Antes (Acoplado) | Ahora (Hexagonal) |
| :--- | :--- | :--- |
| **Lógica de Detalles** | Mezclada en el ORM o en el Router. | Centralizada en `VentaDomain.agregar_detalle()`. |
| **Interacción con Producto** | El Servicio descontaba stock del ORM directamente. | El `VentaService` convierte el Producto a Dominio y llama a `registrar_despacho()`. |
| **Validaciones** | Tipos primitivos (`int`, `datetime`). | **Value Objects** (`CantidadVentaVO`, `FechaVentaVO`) protegen la integridad. |

## 2. Componentes Principales

- **Domain Layer (`venta_domain.py`):**
    - Administra su propia fecha a través de `FechaVentaVO`.
    - Orquesta la creación de detalles validando cantidades mediante `CantidadVentaVO`.
- **Infrastructure Layer (`venta.py` y `venta_repo.py`):**
    - El ORM ahora es un simple mapeador. Implementa `to_domain` y `from_domain` para comunicarse con la lógica pura.
    - El repositorio guarda el "Agregado Completo" (Venta + Detalles) en una sola transacción.
- **Application Layer (`venta_service.py`):**
    - El orquestador por excelencia.
    - Carga Productos -> Los convierte a Dominio -> Descuenta Stock -> Sincroniza al ORM -> Guarda la Venta.

## 3. Beneficios Estratégicos

1. **Integridad Transaccional y de Dominio:** Es imposible que se registre una venta con cantidades negativas o sin descontar el stock, porque el propio `ProductoDomain` detiene la operación si no hay inventario.
2. **Desacoplamiento Total:** La Venta no sabe si se guarda en PostgreSQL o en un archivo. Solo sabe cómo comportarse lógicamente.
3. **Escalabilidad:** Al usar el patrón de "Conversión -> Lógica -> Sincronización", añadir futuros requisitos (ej. cálculo de impuestos o descuentos) solo requerirá tocar la clase pura de Dominio, sin modificar las consultas SQL.

---
*Documentación generada tras la migración de Ventas a Arquitectura Hexagonal y DDD.*
