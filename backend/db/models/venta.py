from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import relationship
from db.base import Base
from core.value_objects import Cantidad, CantidadProductos
from datetime import datetime, timezone


class Venta(Base):
    
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    productos = relationship("VentaProducto", back_populates="venta", cascade="all, delete-orphan")

    def __init__(self, fecha=None):

        self.fecha = fecha or datetime.now(timezone.utc)

    def agregar_producto(self, venta_producto: 'VentaProducto') -> None:

        # Validar cantidad usando Value Object
        cantidad_vo = Cantidad(venta_producto.cantidad)
        
        # Agregar a la lista de productos
        self.productos.append(venta_producto)

    def remover_producto(self, venta_producto: 'VentaProducto') -> None:

        if venta_producto in self.productos:
            self.productos.remove(venta_producto)

    def obtener_cantidad_productos(self) -> int:

        cantidad_vo = CantidadProductos(len(self.productos))
        return cantidad_vo.value

    def tiene_productos(self) -> bool:

        cantidad_vo = CantidadProductos(len(self.productos))
        return not cantidad_vo.es_vacia()

    def obtener_fecha(self) -> datetime:
        """Retorna la fecha de la venta."""
        return self.fecha

    def calcular_total(self) -> float:

        total = 0.0
        for vp in self.productos:
            # Acceder al producto para obtener su precio
            if hasattr(vp, 'producto') and vp.producto:
                precio_venta = vp.producto.precioVenta
                total += vp.cantidad * precio_venta
        return total

    def obtener_cantidad_total_items(self) -> int:

        total_items = sum(vp.cantidad for vp in self.productos)
        # Validar con Value Object
        if total_items > 0:
            CantidadProductos(total_items)
        return total_items