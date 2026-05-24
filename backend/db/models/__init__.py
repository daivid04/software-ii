# db/models/__init__.py

# 1. Los que ya moviste a src (usa rutas desde la raíz del proyecto)
from src.producto.infrastructure.producto import Producto
from src.autopartes.infrastructure.autoparte import Autoparte

# 2. Los que aún viven en db/models (usa rutas relativas al archivo actual)
from .venta import Venta
from .venta_producto import VentaProducto
from .orden import Orden
from .servicio import Servicio
from .orden_servicio import OrdenServicio
from .empleado import Empleado
from .orden_empleado import OrdenEmpleado