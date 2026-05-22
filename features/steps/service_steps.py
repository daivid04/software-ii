"""
Step definitions para H3: Gestión y Control de Atenciones de Servicios
Validación SWEBOK: Partición de Equivalencia y Caja Negra
"""

from behave import given, when, then


# ==================== ESCENARIO 1: AUTOCOMPLETADO Y PERSONALIZACIÓN ====================

@given('Que el administrador prepara una nueva orden de atención vehicular')
def step_admin_preparing_order(context):
    """
    Precondición: El administrador está en el módulo de órdenes de servicio.
    Contrato SWEBOK: Estado previo válido
    """
    context.servicios_disponibles = [
        "Alineación",
        "Cambio de Aceite",
        "Reparación de Motor",
        "Diagnóstico",
        "Reparación de Suspensión"
    ]
    context.admin_ready_service = True
    assert context.admin_ready_service


@when('Selecciona un servicio del catálogo como "reparación de motor"')
def step_select_service(context):
    """
    Acción: Selecciona un servicio válido del catálogo.
    Contrato SWEBOK: Partición de Equivalencia (servicio válido)
    """
    service_name = "Reparación de Motor"
    
    # Buscar el servicio
    context.selected_service = context.testing_api.obtener_servicio_por_nombre(
        service_name
    )
    
    assert context.selected_service is not None, \
        f"Servicio '{service_name}' no encontrado: {context.testing_api.obtener_ultimo_error()}"
    
    context.service_selected = True


@then('El sistema autocompleta la descripción predeterminada de dicho servicio')
def step_autocomplete_description(context):
    """
    Validación: La descripción predeterminada fue autocompleta da.
    Contrato SWEBOK: Autocomplete garantizado (negocio)
    """
    assert context.service_selected, "No se seleccionó un servicio"
    
    # Obtener descripción predeterminada
    description = context.testing_api.obtener_descripcion_servicio(
        context.selected_service.id
    )
    
    assert description, \
        "La descripción predeterminada está vacía"
    
    assert len(description) > 0, \
        "La descripción no fue autocompleta da correctamente"
    
    context.base_description = description


@then('Permite al administrador registrar observaciones adicionales sobre el vehículo')
def step_allow_additional_notes(context):
    """
    Validación: El administrador puede agregar notas adicionales.
    Contrato SWEBOK: Edición permitida (negocio)
    """
    # Simular que el administrador agrega observaciones
    additional_notes = "Vehículo Toyota Corolla 2020, motor con falla de encendido"
    
    # Registrar orden de servicio con notas
    registro_exitoso = context.testing_api.registrar_orden_servicio(
        servicio_id=context.selected_service.id,
        descripcion_adicional=additional_notes
    )
    
    assert registro_exitoso, \
        f"No se pudo registrar la orden: {context.testing_api.obtener_ultimo_error()}"
    
    # Validar que la orden fue registrada correctamente
    orden_registrada = context.testing_api.last_orden_servicio
    assert orden_registrada is not None, "No hay orden registrada"
    assert orden_registrada.servicio_id == context.selected_service.id, \
        "La orden no está vinculada al servicio correcto"
    
    context.order_registered = True


# ==================== ESCENARIO 2: FALTA DE SERVICIO VÁLIDO ====================

@given('Que el administrador registra los detalles de una atención en el taller')
def step_admin_entering_details(context):
    """
    Precondición: El administrador está ingresando detalles de la atención.
    Contrato SWEBOK: Estado previo válido
    """
    context.order_details = {
        "vehiculo": "Mazda 3",
        "cliente": "Juan Pérez",
        "fecha": "2026-05-22"
    }
    context.admin_entering_details = True
    assert context.admin_entering_details


@when('Intenta confirmar la orden sin asignar la categoría del servicio realizado')
def step_attempt_save_without_service(context):
    """
    Acción: Intenta guardar una orden sin seleccionar servicio.
    Contrato SWEBOK: Caja Negra (validación de campo obligatorio)
    """
    # Intentar registrar sin servicio (servicio_id = None)
    context.registro_sin_servicio = context.testing_api.registrar_orden_servicio(
        servicio_id=None,  # Simular selección vacía
        descripcion_adicional="Sin especificar"
    )
    
    # Debería fallar
    context.save_blocked = context.registro_sin_servicio is False


@then('El sistema bloquea el registro de la atención')
def step_block_save(context):
    """
    Validación: El guardado fue bloqueado.
    Contrato SWEBOK: Restricción activa (validación)
    """
    assert context.save_blocked is True, \
        "El sistema permitió guardar sin seleccionar servicio"


@then('Exige la selección de un servicio válido del catálogo para mantener el control')
def step_demand_service_selection(context):
    """
    Validación: Se emitió un mensaje exigiendo servicio válido.
    Contrato SWEBOK: Mensaje de error específico (negocio)
    """
    error_msg = context.testing_api.obtener_ultimo_error()
    assert error_msg, "No hay mensaje de error registrado"
    
    # El mensaje debe indicar que falta el servicio
    assert ("servicio" in error_msg.lower() or 
            "válido" in error_msg.lower()), \
        f"Mensaje incorrecto: {error_msg}"
