Feature: Gestión y Venta de Producto

  Scenario: Identificación exitosa de un producto para su gestión o venta
    Given Que el administrador se encuentra en un módulo del sistema que requiere un artículo
    When Escanea un código de barras válido y registrado con la pistola lectora
    Then El sistema captura de forma síncrona la lectura del producto activo
    And Muestra en pantalla sus detalles, precio y ubicación exacta en el taller
    And Habilita el ítem para su rápida búsqueda, actualización o venta

  Scenario: Intento de escaneo de un código inexistente o lectura defectuosa
    Given Que el administrador intenta procesar un producto con la pistola lectora
    When Escanea un código de barras no registrado o con lectura incompleta
    Then El sistema bloquea la carga de información en la interfaz
    And Emite una alerta indicando que el producto no fue encontrado o el formato es inválido
    And Mantiene la pantalla limpia y lista para recibir un nuevo escaneo
