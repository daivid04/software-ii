from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base



class VentaProducto(Base):
    __tablename__ = "venta_producto"

    id = Column(Integer, primary_key=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)

    producto = relationship("Producto", back_populates="ventas")
    venta = relationship("Venta", back_populates="productos")