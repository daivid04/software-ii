# Plan de Pruebas Caja Negra

Este plan describe las pruebas de caja negra del sistema. Se toma como base la guia SWEBOK v4.0a (Washizaki, 2025) con las tecnicas de particion de equivalencia y valores limite. El objetivo es validar el comportamiento observable de la API sin mirar el codigo interno.

## 1. Alcance
- Modulos cubiertos: empleados, autopartes, productos, servicios, ordenes y ventas.
- Capa probada: rutas HTTP de la API.
- Se prueba con datos reales de entrada y salida (request/response).

## 2. Fuera de alcance
- Pruebas de rendimiento o carga.
- Pruebas de seguridad profunda (solo se valida que la API responda con permisos).
- Pruebas de interfaz web.

## 3. Tecnicas aplicadas
- Particion de equivalencia: entradas validas e invalidas por regla de negocio.
- Valores limite: limites minimos y maximos en campos clave.

## 4. Criterios de aceptacion
- Las rutas deben responder con estado 200 o 201 en escenarios validos.
- Las rutas deben responder con 400 o 422 en escenarios invalidos segun la regla aplicada.
- No se aceptan datos fuera del glosario del negocio (estado de empleado, precios, etc.).

## 5. Evidencia en codigo
Los casos se encuentran en:
- tests/caja_negra/test_empleado_caja_negra.py
- tests/caja_negra/test_autoparte_caja_negra.py
- tests/caja_negra/test_producto_caja_negra.py
- tests/caja_negra/test_servicio_caja_negra.py
- tests/caja_negra/test_orden_caja_negra.py
- tests/caja_negra/test_venta_caja_negra.py

## 6. Ejecucion
Desde la carpeta backend:

python -m pytest tests/caja_negra/
