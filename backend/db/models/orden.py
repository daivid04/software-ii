from sqlalchemy import Column, Integer, String, Date
from db.base import Base
from sqlalchemy.orm import relationship
from core.value_objects import Precio

class Orden(Base):
    __tablename__ = "ordenes"

    id = Column(Integer, primary_key=True)
    garantia = Column(Integer, nullable=False)
    estadoPago = Column(String, nullable=False)
    precio = Column(Integer, nullable=False)
    fecha = Column(Date, nullable=False)

    servicios = relationship("OrdenServicio", back_populates="orden")
    empleados = relationship("OrdenEmpleado", back_populates="orden")

    @staticmethod
    def validate_precio(value: float) -> Precio:
        return Precio(value)

    def agregar_item(self, precio_unitario: float):
        # Validar precio
        precio_vo = Precio(precio_unitario)
        # Actualizar total (invariante: total consistente)
        self.precio += precio_vo.value