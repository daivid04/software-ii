# Plan de Pruebas de Mutacion

Este plan describe las pruebas de mutacion del dominio. Se toma como base la guia SWEBOK v4.0a (Washizaki, 2025). El objetivo es comprobar que las reglas del negocio se mantienen firmes si ocurre un cambio accidental en el codigo (mutante).

## 1. Alcance
- Modulos cubiertos: empleados, autopartes, productos, servicios, ordenes y ventas.
- Capa probada: reglas del dominio y objetos de valor.

## 2. Fuera de alcance
- Integraciones con base de datos.
- API HTTP o autenticacion.
- Rendimiento.

## 3. Estrategia
- Se crean entradas que deberian fallar si se rompe una regla.
- Cada prueba intenta "matar" un mutante tipico (por ejemplo, quitar una validacion).

## 4. Criterios de aceptacion
- Las reglas del dominio deben lanzar ValueError cuando los datos son invalidos.
- No se permiten precios negativos, cantidades en cero, estados no permitidos, ni fechas futuras.

## 5. Evidencia en codigo
Los casos se encuentran en:
- tests/mutacion/test_empleado_mutacion.py
- tests/mutacion/test_autoparte_mutacion.py
- tests/mutacion/test_producto_mutacion.py
- tests/mutacion/test_servicio_mutacion.py
- tests/mutacion/test_orden_mutacion.py
- tests/mutacion/test_venta_mutacion.py

## 6. Ejecucion
Desde la carpeta backend:

python -m pytest tests/mutacion/
