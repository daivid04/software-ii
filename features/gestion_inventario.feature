Feature: Control de Inventario de Productos

  Scenario: Registro exitoso dentro de la capacidad operativa
    Given El taller cuenta con un inventario activo de 200 productos registrados.
    When El administrador registra una nueva pieza de repuesto con su marca, modelo y año.
    Then El sistema debería confirmar que el registro se realizó correctamente.
    And El recuento total del inventario debe reflejar 201 artículos activos.

  Scenario: El registro está bloqueado debido al límite máximo de capacidad.
    Given El inventario del taller ya contiene 300 productos activos.
    When El administrador intenta registrar un aceite o repuesto adicional.
    Then El sistema debería denegar el registro del nuevo producto.
    And El sistema debería informar al administrador de que se ha alcanzado el límite máximo de capacidad.
    And El recuento de inventario debe mantenerse exactamente en 300 productos.
