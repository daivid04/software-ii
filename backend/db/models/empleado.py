from sqlalchemy import Column, Integer, String
from db.base import Base
from sqlalchemy.orm import relationship
from db.models.value_objects import InformacionEmpleadoVO, EstadoEmpleadoVO

class Empleado(Base):
    __tablename__ = "empleados"

    id = Column(Integer, primary_key=True)
    nombres = Column(String, nullable=False, unique=True)
    apellidos = Column(String, nullable=False)
    estado = Column(String, nullable=False, default="activo")
    especialidad = Column(String, nullable=False)

    ordenes = relationship("OrdenEmpleado", back_populates="empleado")

    # ==========================================
    # LÓGICA DE DOMINIO 
    # ==========================================

    def actualizar_informacion(self, nombres: str, apellidos: str, especialidad: str):
        """El Agregado valida y asigna sus datos básicos mediante su Value Object"""
        info_vo = InformacionEmpleadoVO(nombres=nombres, apellidos=apellidos, especialidad=especialidad)
        self.nombres = info_vo.nombres
        self.apellidos = info_vo.apellidos
        self.especialidad = info_vo.especialidad

    def cambiar_estado(self, estado: str):
        """Modifica el estado laboral usando validación de dominio"""
        estado_vo = EstadoEmpleadoVO(valor=estado)
        self.estado = estado_vo.valor.lower()