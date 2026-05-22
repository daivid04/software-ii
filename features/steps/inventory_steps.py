"""
Step definitions para H1: Control de Inventario de Productos
Validación SWEBOK: Partición de Equivalencia y Valores Límite
"""

from behave import given, when, then


# ==================== ESCENARIO 1: REGISTRO EXITOSO ====================

@given('El taller cuenta con un inventario activo de {count} productos registrados.')
def step_init_inventory(context, count):
    """
    Precondición: Inicializa el inventario con `count` productos válidos.
    Contrato SWEBOK: Partición de Equivalencia (rango 200-300)
    """
    count = int(count)
    context.testing_api.inicializar_inventario(count)
    context.initial_count = count
    assert context.testing_api.obtener_conteo_productos() == count, \
        f"Esperaba {count} productos, pero hay {context.testing_api.obtener_conteo_productos()}"


@when('El administrador registra una nueva pieza de repuesto con su marca, modelo y año.')
def step_register_producto(context):
    """
    Acción: Registra un nuevo producto con datos válidos.
    Contrato SWEBOK: Valores válidos de marca, modelo, año
    """
    context.registro_exitoso = context.testing_api.registrar_producto(
        marca="Bosch",
        modelo="F026T015",
        año="2024"
    )
    assert context.registro_exitoso, \
        f"Error al registrar: {context.testing_api.obtener_ultimo_error()}"


@then('El sistema debería confirmar que el registro se realizó correctamente.')
def step_confirm_registro(context):
    """
    Validación: El registro fue confirmado exitosamente.
    Contrato SWEBOK: Estado final válido (producto creado)
    """
    assert context.registro_exitoso is True, \
        "El sistema no confirmó el registro exitoso"
    assert context.testing_api.last_producto is not None, \
        "No hay producto registrado en contexto"


@then('El recuento total del inventario debe reflejar {expected_count} artículos activos.')
def step_verify_count(context, expected_count):
    """
    Validación: El contador se incrementó en 1.
    Contrato SWEBOK: Valor exacto esperado (200 → 201)
    """
    expected_count = int(expected_count)
    actual_count = context.testing_api.obtener_conteo_productos()
    assert actual_count == expected_count, \
        f"Esperaba {expected_count} productos, pero hay {actual_count}"


# ==================== ESCENARIO 2: CAPACIDAD MÁXIMA EXCEDIDA ====================

@given('El inventario del taller ya contiene {count} productos activos.')
def step_init_inventory_max(context, count):
    """
    Precondición: Llena inventario hasta el límite máximo (300).
    Contrato SWEBOK: Valores Límite (límite superior = 300)
    """
    count = int(count)
    context.testing_api.inicializar_inventario(count)
    context.max_count = count
    assert context.testing_api.obtener_conteo_productos() == count, \
        f"No se pudo inicializar inventario a {count}"


@when('El administrador intenta registrar un aceite o repuesto adicional.')
def step_attempt_registro_exceed(context):
    """
    Acción: Intenta agregar un producto cuando el límite está alcanzado.
    Contrato SWEBOK: Violación de restricción de capacidad
    """
    context.registro_rechazado = not context.testing_api.registrar_producto(
        marca="Shell",
        modelo="Helix",
        año="2024"
    )
    # Nota: Si retorna False, significa que fue rechazado (lo que queremos)


@then('El sistema debería denegar el registro del nuevo producto.')
def step_verify_rejection(context):
    """
    Validación: El sistema bloqueó el registro.
    Contrato SWEBOK: Restricción activa (sin excepciones)
    """
    assert context.registro_rechazado is True, \
        "El sistema permitió un registro que debía ser rechazado"


@then('El sistema debería informar al administrador de que se ha alcanzado el límite máximo de capacidad.')
def step_verify_error_message(context):
    """
    Validación: Se emitió alerta clara sobre límite alcanzado.
    Contrato SWEBOK: Mensaje de error específico (negocio)
    """
    error_msg = context.testing_api.obtener_ultimo_error()
    assert error_msg, "No hay mensaje de error registrado"
    assert "límite máximo" in error_msg.lower() or "300" in error_msg, \
        f"Mensaje de error incorrecto: {error_msg}"


@then('El recuento de inventario debe mantenerse exactamente en {expected_count} productos.')
def step_verify_count_unchanged(context, expected_count):
    """
    Validación: El contador NO cambió (se mantiene en 300).
    Contrato SWEBOK: Integridad de datos (atomicidad)
    """
    expected_count = int(expected_count)
    actual_count = context.testing_api.obtener_conteo_productos()
    assert actual_count == expected_count, \
        f"El inventario cambió a {actual_count}, esperaba {expected_count}"
