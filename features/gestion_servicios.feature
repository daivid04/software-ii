Feature: Gestión y Control de Atenciones de Servicios

  Scenario: Autocompletado y personalización de la descripción de un servicio
    Given Que el administrador prepara una nueva orden de atención vehicular
    When Selecciona un servicio del catálogo como "reparación de motor"
    Then El sistema autocompleta la descripción predeterminada de dicho servicio
    And Permite al administrador registrar observaciones adicionales sobre el vehículo

  Scenario: Intento de registro de atención sin especificar un servicio válido
    Given Que el administrador registra los detalles de una atención en el taller
    When Intenta confirmar la orden sin asignar la categoría del servicio realizado
    Then El sistema bloquea el registro de la atención
    And Exige la selección de un servicio válido del catálogo para mantener el control
