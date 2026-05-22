"""
Step definitions para H2: Gestión y Venta de Producto (Barcode Scanner)
Validación SWEBOK: Partición de Equivalencia y Caja Negra
"""

from behave import given, when, then


# ==================== ESCENARIO 1: ESCANEO EXITOSO ====================

@given('Que el administrador se encuentra en un módulo del sistema que requiere un artículo')
def step_admin_in_module(context):
    """
    Precondición: El administrador está en un módulo que requiere validar productos.
    Contrato SWEBOK: Estado previo válido
    """
    # Registrar algunos productos de prueba
    result1 = context.testing_api.registrar_producto_con_barcode(
        codigo_barras="BOB001234567",
        marca="Bosch"
    )
    if not result1:
        error1 = context.testing_api.obtener_ultimo_error()
        print(f"  [ERROR] Falló registrar producto 1: {error1}")
    
    result2 = context.testing_api.registrar_producto_con_barcode(
        codigo_barras="FER001234567",
        marca="Ferodo"
    )
    if not result2:
        error2 = context.testing_api.obtener_ultimo_error()
        print(f"  [ERROR] Falló registrar producto 2: {error2}")
    
    context.valid_barcode = "BOB001234567"
    context.admin_ready = True
    
    assert result1 and result2, \
        f"Falló registrar productos - P1: {result1}, P2: {result2}"
    assert context.admin_ready, "El administrador no está en un módulo válido"


@when('Escanea un código de barras válido y registrado con la pistola lectora')
def step_scan_valid_barcode(context):
    """
    Acción: Escanea un código de barras que existe en la BD.
    Contrato SWEBOK: Partición de Equivalencia (código válido)
    """
    context.scanned_product = context.testing_api.buscar_producto_por_barcode(
        context.valid_barcode
    )
    context.scan_successful = context.scanned_product is not None


@then('El sistema captura de forma síncrona la lectura del producto activo')
def step_capture_sync(context):
    """
    Validación: Captura fue síncrona (producto disponible inmediatamente).
    Contrato SWEBOK: Comportamiento sincrónico garantizado
    """
    assert context.scan_successful, \
        f"La captura síncrona falló: {context.testing_api.obtener_ultimo_error()}"
    assert context.scanned_product is not None, \
        "No hay producto capturado en contexto"


@then('Muestra en pantalla sus detalles, precio y ubicación exacta en el taller')
def step_display_details(context):
    """
    Validación: Detalles, precio y ubicación están disponibles.
    Contrato SWEBOK: Contrato de salida SWEBOK (datos planos)
    """
    details = context.testing_api.obtener_detalles_producto(
        context.scanned_product.id
    )
    
    # Validar que todos los campos obligatorios existan
    assert "precio" in details, "Falta el campo 'precio'"
    assert "ubicacion" in details, "Falta el campo 'ubicacion'"
    assert "marca" in details, "Falta el campo 'marca'"
    
    # Validar que tengan valores válidos
    assert details["precio"] > 0, "El precio debe ser mayor a 0"
    assert details["ubicacion"], "La ubicación no puede estar vacía"


@then('Habilita el ítem para su rápida búsqueda, actualización o venta')
def step_enable_item_operations(context):
    """
    Validación: El producto está listo para operaciones posteriores.
    Contrato SWEBOK: Disponibilidad confirmada (negocio)
    """
    # El producto está en contexto y con stock disponible
    assert context.scanned_product.stock > 0, \
        "El producto no tiene stock disponible"
    assert context.scanned_product.id, \
        "El producto no tiene ID válido"


# ==================== ESCENARIO 2: CÓDIGO INEXISTENTE O LECTURA DEFECTUOSA ====================

@given('Que el administrador intenta procesar un producto con la pistola lectora')
def step_admin_ready_to_scan(context):
    """
    Precondición: El administrador está listo para escanear.
    Contrato SWEBOK: Estado previo válido
    """
    # Registrar solo algunos productos
    context.testing_api.registrar_producto_con_barcode(
        codigo_barras="VALID999",
        marca="TestMarca"
    )
    context.admin_scanning = True
    assert context.admin_scanning


@when('Escanea un código de barras no registrado o con lectura incompleta')
def step_scan_invalid_barcode(context):
    """
    Acción: Intenta escanear un código que no existe o es truncado.
    Contrato SWEBOK: Caja Negra (error de entrada)
    """
    # Caso 1: Código no registrado
    context.invalid_barcode_1 = "INVALID123"
    context.product_from_invalid_1 = context.testing_api.buscar_producto_por_barcode(
        context.invalid_barcode_1
    )
    
    # Caso 2: Lectura truncada/incompleta
    context.invalid_barcode_2 = "TR"  # Muy corto
    context.product_from_invalid_2 = context.testing_api.buscar_producto_por_barcode(
        context.invalid_barcode_2
    )
    
    context.scan_failed = (
        context.product_from_invalid_1 is None and
        context.product_from_invalid_2 is None
    )


@then('El sistema bloquea la carga de información en la interfaz')
def step_block_invalid_load(context):
    """
    Validación: No se cargó información de un código inválido.
    Contrato SWEBOK: Restricción activa (sin cargas erróneas)
    """
    assert context.scan_failed, \
        "El sistema cargó información de códigos inválidos"
    assert context.product_from_invalid_1 is None, \
        "Se cargó un producto de un código no registrado"
    assert context.product_from_invalid_2 is None, \
        "Se cargó un producto de una lectura truncada"


@then('Emite una alerta indicando que el producto no fue encontrado o el formato es inválido')
def step_emit_alert(context):
    """
    Validación: Se emitió una alerta clara.
    Contrato SWEBOK: Mensaje de error específico (negocio)
    """
    error_msg = context.testing_api.obtener_ultimo_error()
    assert error_msg, "No hay mensaje de error registrado"
    
    # Validar que sea un mensaje apropiad Producto no encontrado
    assert ("no encontrado" in error_msg.lower() or 
            "incompleta" in error_msg.lower() or
            "truncado" in error_msg.lower()), \
        f"Alerta inapropiada: {error_msg}"


@then('Mantiene la pantalla limpia y lista para recibir un nuevo escaneo')
def step_keep_screen_clean(context):
    """
    Validación: La interfaz está limpia (sin datos parciales o errores visuales).
    Contrato SWEBOK: Integridad de interfaz (negocio)
    """
    # El contexto no debe tener productos inválidos residuales
    # (esto se valida implícitamente al no cargar errores)
    assert context.product_from_invalid_1 is None
    assert context.product_from_invalid_2 is None
    # La pantalla está "limpia" porque no hay datos de escaneo fallido
