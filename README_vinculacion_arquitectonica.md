| Nombre de Escenario Gherkin | Puerto Primario / Caso de Uso | Técnica SWEBOK Aplicada |
|-----------------------------|-------------------------------|-------------------------|
| Registro exitoso dentro de la capacidad operativa | `registrar_producto(marca, modelo, año)` → ProductoService.create_producto() | **Caja Blanca**: Partición de Equivalencia |
| El registro está bloqueado debido al límite máximo de capacidad | `registrar_producto(marca, modelo, año)` → validación de límite | **Caja Blanca**: Valores Límite |
| Identificación exitosa de un producto para su gestión o venta | `buscar_producto_por_barcode(codigo_barras)` → ProductoService.get_by_barcode() | **Caja Blanca**: Partición de Equivalencia |
| Intento de escaneo de un código inexistente o lectura defectuosa | `buscar_producto_por_barcode(codigo_barras)` → validación de formato/existencia | **Caja Negra**: Manejo de excepciones |
| Autocompletado y personalización de la descripción de un servicio | `registrar_orden_servicio(servicio_id, descripcion_adicional)` → OrdenService.create() | **Caja Blanca**: Partición de Equivalencia |
| Intento de registro de atención sin especificar un servicio válido | `registrar_orden_servicio(servicio_id=None)` → validación de contrato | **Caja Negra**: Validación de campo obligatorio |

##  Cómo ejecutar los tests con Behave

### Prerequisitos
```bash
# Activar el entorno virtual
c:\Users\bianc\software-ii\.venv\Scripts\activate
```

### Ejecutar todos los tests
```bash
cd c:\Users\bianc\software-ii
$env:PYTHONPATH="c:\Users\bianc\software-ii\backend"
python -m behave features/
```

### Ejecutar una feature específica
```bash
# Solo inventario
python -m behave features/gestion_inventario.feature

# Solo barcode
python -m behave features/lectura_barcode.feature

# Solo servicios
python -m behave features/gestion_servicios.feature
```

### Ejecutar un escenario específico
```bash
# H1.1: Registro exitoso
python -m behave features/gestion_inventario.feature:3

# H1.2: Bloqueo por límite
python -m behave features/gestion_inventario.feature:9
```

### Opciones útiles de Behave
```bash
# Formato detallado
python -m behave features/ --format plain

# Sin capturar output (ver prints)
python -m behave features/ --no-capture

# Color desactivado
python -m behave features/ --no-color

# Mostrar pasos pasados
python -m behave features/ --format progress
```

### Resultado esperado
```
3 features passed, 0 failed, 0 skipped
6 scenarios passed, 0 failed, 0 skipped
27 steps passed, 0 failed, 0 skipped
Took 0min 2.311s
```
