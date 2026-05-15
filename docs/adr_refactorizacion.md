# ADR: Refactorización Táctica del MVP con Domain-Driven Design

## Contexto
Durante el análisis del sistema actual, se detectó anemia de dominio: los modelos (ej. `Empleado`, `Producto`) eran solo estructuras de datos con atributos y getters/setters, mientras que la lógica de negocio estaba concentrada en clases Service (ej. `OrdenService`). Esto viola principios de DDD, ya que las reglas importantes (ej. validación de precios >0, consistencia de totales en órdenes) no estaban encapsuladas en el dominio, llevando a posibles inconsistencias y dificultad para mantener invariantes.

## Decisión
Decidimos implementar Value Objects (VOs) para tipos primitivos y un Aggregate Root (AR) para la entidad principal, moviendo lógica de negocio al dominio:
- **Value Objects**: `Email` (valida formato) y `Precio` (valida >0), inmutables y comparables por valor.
- **Aggregate Root**: `Orden`, con métodos para proteger invariantes (ej. `agregar_item` actualiza total consistentemente) y validar datos (ej. `validate_precio`).
- **Movimiento de lógica**: Validaciones de precio movidas de `OrdenService` a `Orden` para reducir anemia.

## Justificación
Esta decisión asegura la protección de invariantes críticos (ej. precios válidos y totales consistentes) y encapsula reglas de negocio en el dominio, siguiendo Domain-Driven Design (Vernon, 2013). Mejora coherencia, mantenibilidad y evita errores de concurrencia, transformando el sistema de una estructura de datos a un modelo rico en comportamiento.