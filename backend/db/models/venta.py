from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import relationship
from db.base import Base



class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, nullable=False)

    productos = relationship("VentaProducto", back_populates="venta")