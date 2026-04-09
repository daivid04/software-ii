from sqlalchemy import Column, Integer, String
from db.base import Base
from sqlalchemy.orm import relationship

class Empleado(Base):
    __tablename__ = "empleados"

    id = Column(Integer, primary_key=True)
    nombres = Column(String, nullable=False, unique=True)
    apellidos = Column(String, nullable=False)
    estado = Column(String, nullable=False, default="activo")
    especialidad = Column(String, nullable=False)

    ordenes = relationship("OrdenEmpleado", back_populates="empleado")