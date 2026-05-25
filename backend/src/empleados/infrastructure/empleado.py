from sqlalchemy import Column, Integer, String
from db.base import Base
from sqlalchemy.orm import relationship
from src.empleados.domain.empleado_domain import EmpleadoDomain

class Empleado(Base):
    __tablename__ = "empleados"

    id = Column(Integer, primary_key=True)
    nombres = Column(String, nullable=False, unique=True)
    apellidos = Column(String, nullable=False)
    estado = Column(String, nullable=False, default="activo")
    especialidad = Column(String, nullable=False)

    ordenes = relationship("OrdenEmpleado", back_populates="empleado")


    def to_domain(self) -> EmpleadoDomain:
        return EmpleadoDomain(
            id=self.id,
            nombres=self.nombres,
            apellidos=self.apellidos,
            estado=self.estado,
            especialidad=self.especialidad
        )

    def from_domain(self, domain: EmpleadoDomain):
        self.nombres = domain.nombres
        self.apellidos = domain.apellidos
        self.estado = domain.estado
        self.especialidad = domain.especialidad