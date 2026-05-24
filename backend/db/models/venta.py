from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import relationship
from db.base import Base
from datetime import datetime
from src.shared.domain.value_objects import CantidadVentaVO, FechaVentaVO



class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, nullable=False)

    productos = relationship("VentaProducto", back_populates="venta")

    # ==========================================
    # LÓGICA DE DOMINIO 
    # ==========================================

    def inicializar_fecha(self, fecha_mecanica: datetime):
        """Asigna la fecha validándola a través de su Value Object"""
        fecha_vo = FechaVentaVO(fecha_mecanica)
        self.fecha = fecha_vo.valor

    def agregar_detalle(self, producto, cantidad: int, entidad_venta_producto_class):
        """La Venta orquesta la adición validando con CantidadVentaVO"""
        # 1. Validamos la cantidad internamente con el Value Object
        cantidad_vo = CantidadVentaVO(cantidad)
        
        # 2. El Producto (otro Agregado) valida y descuenta su propio stock
        producto.registrar_despacho(cantidad_vo.valor)
        
        # 3. La Venta crea su propia entidad interna (Detalle) usando el valor validado
        nuevo_detalle = entidad_venta_producto_class(
            producto_id=producto.id,
            cantidad=cantidad_vo.valor
        )
        self.productos.append(nuevo_detalle)