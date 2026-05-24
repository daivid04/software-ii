# Refactorización Backend - Producto (DDD - Lenguaje Ubicuo)


## 🔄 Cambios Realizados
---

### 3. **Repositorio** (`backend/repositories/producto_repo.py`)

#### Cambios Principales:
**Métodos técnicos → Métodos con lenguaje de negocio**

| Método Anterior | Método Nuevo | Propósito (Lenguaje de Negocio) |
|-----------------|--------------|--------------------------------|
| `create()` | `registrar_producto()` | Registrar un nuevo producto en el catálogo |
| `get_all()` | `listar_catalogo_productos()` | Listar todos los productos disponibles |
| `get_by_id()` | `consultar_producto()` | Consultar datos de un producto específico |
| `get_by_name()` | `buscar_producto_por_nombre()` | Buscar producto por su nombre |
| `get_by_barcode()` | `escanear_codigo_barras()` | Escanear código de barras (punto de venta) |
| `update()` | `actualizar_inventario_producto()` | Actualizar stock y precios del producto |
| `delete()` | `dar_de_baja_producto()` | Dar de baja un producto del catálogo |

#### Código Actualizado:

**Métodos renombrados y su propósito:**
- `registrar_producto()` → Registra un nuevo producto en el catálogo
- `listar_catalogo_productos()` → Lista todos los productos del catálogo
- `consultar_producto()` → Consulta un producto por su ID
- `buscar_producto_por_nombre()` → Busca un producto por nombre
- `escanear_codigo_barras()` → Escanea un código de barras y devuelve el producto
- `actualizar_inventario_producto()` → Actualiza el inventario del producto (precios, stock, etc.)
- `dar_de_baja_producto()` → Da de baja un producto del catálogo

---

### 4. **Servicio de Negocio** (`backend/services/producto_service.py`)

#### Cambios Principales:
**Métodos técnicos → Métodos con lenguaje de negocio**

| Método Anterior | Método Nuevo | Propósito |
|-----------------|--------------|-----------|
| `create_producto()` | `registrar_nuevo_producto()` | Registrar nuevo producto con validaciones |
| `list_productos()` | `obtener_catalogo_completo()` | Obtener catálogo completo |
| `get_by_id()` | `consultar_producto_disponible()` | Consultar si un producto está disponible |
| `get_by_name()` | `buscar_producto_por_nombre()` | Buscar por nombre |
| `get_by_barcode()` | `escanear_codigo_barras()` | Escanear código de barras |
| `update_producto()` | `actualizar_stock_y_precios()` | Actualizar inventario |
| `delete_producto()` | `dar_de_baja_producto()` | Dar de baja producto |

#### Código Actualizado:

**Métodos renombrados y su propósito:**
- `registrar_nuevo_producto()` → Registra un nuevo producto en el sistema
- `obtener_catalogo_completo()` → Obtiene el catálogo completo de productos
- `consultar_producto_disponible()` → Consulta si un producto está disponible
- `buscar_producto_por_nombre()` → Busca un producto por nombre en el catálogo
- `escanear_codigo_barras()` → Escanea un código de barras para obtener el producto
- `actualizar_stock_y_precios()` → Actualiza el stock y precios del producto
- `dar_de_baja_producto()` → Da de baja un producto del sistema


---

#### Cambios Específicos:

| Cambio | Antes | Después |
|--------|-------|---------|
| Función endpoint (POST) | `create_producto()` | `crear_nuevo_producto()` |
| Llamada a servicio | `service.create_producto()` | `service.registrar_nuevo_producto()` |
| Función endpoint (GET /) | `list_productos()` | Actualizada |
| Llamada a servicio | `service.list_productos()` | `service.obtener_catalogo_completo()` |
| Ruta código de barras | `/barcode/{codBarras}` | `/codigo-barras/{codigo_barras}` |
| Función endpoint | `get_producto_by_barcode()` | `escanear_codigo_barras()` |
| Llamada a servicio | `service.get_by_barcode()` | `service.escanear_codigo_barras()` |
| Función endpoint (GET /{id}) | Actualizada | Actualizada |
| Llamada a servicio | `service.get_by_id()` | `service.consultar_producto_disponible()` |
| Función endpoint (PUT) | `update_producto()` | `actualizar_stock_y_precios()` |
| Llamada a servicio | `service.update_producto()` | `service.actualizar_stock_y_precios()` |
| Función endpoint (DELETE) | `delete_producto()` | `dar_de_baja_producto()` |
| Llamada a servicio | `service.delete_producto()` | `service.dar_de_baja_producto()` |
| Mensaje respuesta | "Producto eliminado" | "Producto dado de baja" |




