Feature: Gestión y Control de Atenciones de Servicios

  Scenario: Autocompletado y personalización de la descripción de un servicio
    Given que el administrador prepara una nueva orden de atención vehicular
    When selecciona un servicio del catálogo como "reparación de motor"
    Then el sistema autocompleta la descripción predeterminada de dicho servicio
    And permite al administrador registrar observaciones adicionales sobre el vehículo

  Scenario: Intento de registro de atención sin especificar un servicio válido
    Given que el administrador registra los detalles de una atención en el taller
    When intenta confirmar la orden sin asignar la categoría del servicio realizado
    Then el sistema bloquea el registro de la atención
    And exige la selección de un servicio válido del catálogo para mantener el control
