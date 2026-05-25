# db/models/__init__.py

# 1. Los que ya moviste a src (usa rutas desde la raíz del proyecto)
from src.producto.infrastructure.producto import Producto
from src.autopartes.infrastructure.autoparte import Autoparte
from src.ventas.infrastructure.venta import Venta
from src.servicios.infrastructure.servicio import Servicio
from src.ventas.infrastructure.venta_producto import VentaProducto
from src.ordenes.infrastructure.orden import Orden
from src.ordenes.infrastructure.orden_servicio import OrdenServicio
from src.ordenes.infrastructure.orden_empleado import OrdenEmpleado
from src.empleados.infrastructure.empleado import Empleado
