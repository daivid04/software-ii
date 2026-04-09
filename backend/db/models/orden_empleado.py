from sqlalchemy import Column, Integer, ForeignKey
from db.base import Base
from sqlalchemy.orm import relationship

class OrdenEmpleado(Base):
    __tablename__ = "orden_empleado"

    id = Column(Integer, primary_key=True)
    orden_id = Column(Integer, ForeignKey("ordenes.id"), nullable=False)
    empleado_id = Column(Integer, ForeignKey("empleados.id"), nullable=False)

    empleado = relationship("Empleado", back_populates="ordenes")
    orden = relationship("Orden", back_populates="empleados")