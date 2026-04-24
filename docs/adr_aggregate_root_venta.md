# ADR 003: Segundo Aggregate Root Venta y Value Objects de Cantidad

## Contexto

Tras implementar exitosamente **Orden como Aggregate Root** (ADR 002), surgió la oportunidad de aplicar el mismo patrón de Domain-Driven Design a **Venta**.

**Venta en el sistema:**

- Representa una transacción de venta de productos
- Tiene relación con VentaProducto (tabla intermedia)
- Registra fecha de la transacción
- Agrupa múltiples productos vendidos

**Reglas de negocio identificadas:**

1. **Cantidad válida:** Solo se pueden vender cantidades > 0 de cada producto (máximo 10,000)
2. **Consistencia de productos:** La venta debe mantener coherencia en sus productos agregados
3. **Cálculo de totales:** El total debe ser suma de (cantidad × precio unitario)

**Problema detectado:** Sin encapsulación, es posible agregar cantidades inválidas directamente a `venta.productos`, violando invariantes del dominio.

## Decisión

Decidimos implementar **Venta como segundo Aggregate Root** con validación encapsulada usando 2 nuevos **Value Objects**:

- **Value Objects**:
  - `Cantidad`: Valida cantidad individual (1-10,000), inmutable, comparable por valor
  - `CantidadProductos`: Valida cantidad de tipos diferentes (0-infinito), puede estar vacía, inmutable
- **Aggregate Root**: `Venta`, con métodos para proteger invariantes (ej. `agregar_producto` valida cantidad) y consultar información (ej. `calcular_total`, `obtener_cantidad_productos`)

- **Movimiento de lógica**: Validación de cantidades movida de `VentaService` a `Venta`, cálculo de total encapsulado en el modelo

## Justificación

Esta decisión asegura la protección de invariantes críticos (ej. cantidades válidas, consistencia de productos) y encapsula reglas de negocio en el dominio, siguiendo Domain-Driven Design (Vernon, 2013).

**Beneficios realizados:**

- ✅ **Integridad**: Imposible agregar cantidades ≤ 0 o > 10,000
- ✅ **Coherencia**: Venta y Orden aplican DDD consistentemente
- ✅ **Testabilidad**: Pruebas unitarias sin dependencia de BD
- ✅ **Mantenibilidad**: Cambios centralizados en el modelo
- ✅ **Escalabilidad**: Preparado para Eventos de Dominio

**Comparación Orden vs Venta:**

| Aspecto             | Orden              | Venta           |
| ------------------- | ------------------ | --------------- |
| Aggregate Root      | Sí                 | Sí              |
| Value Objects       | 4                  | 2               |
| Métodos principales | 7                  | 8               |
| Invariante          | Precio consistente | Cantidad válida |
| Cambios de estado   | Dinámico           | Estático        |

## Consecuencias

**Positivas:**

- Validación automática en construcción
- Integridad garantizada de invariantes
- Código más legible y mantenible
- Compatible con eventos de dominio

**Negativas:**

- Mayor complejidad inicial
- Más objetos a instanciar
- Curva de aprendizaje para el equipo

**Mitigación:** Documentación clara, ejemplos de uso, tests como guías

## Siguiente Paso

Una vez validada esta refactorización en tests, en la **Semana 4** se implementarán **Eventos de Dominio** para capturar cambios importantes (ej. `VentaCompletadaEvent`) y habilitar arquitecturas más complejas como Event Sourcing y CQRS.

---

**Referencias:**

- "Implementing Domain-Driven Design" - Vaughn Vernon, 2013
- "Domain-Driven Design" - Eric Evans, 2003
- ADR 002: Aggregate Root Orden (este proyecto)
