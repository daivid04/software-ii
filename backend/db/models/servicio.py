from sqlalchemy import Column, Integer, String
from db.base import Base
from sqlalchemy.orm import relationship
from db.models.value_objects import InformacionServicioVO

class Servicio(Base):
    __tablename__ = "servicios"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False, unique=True)
    descripcion = Column(String, nullable=False, default="")

    ordenes = relationship("OrdenServicio", back_populates="servicio")


    # ==========================================
    # LÓGICA DE DOMINIO 
    # ==========================================

    def actualizar_informacion(self, nombre: str, descripcion: str):
        """El Agregado delega la validación de sus datos al Value Object"""
        info_vo = InformacionServicioVO(nombre=nombre, descripcion=descripcion)
        self.nombre = info_vo.nombre
        self.descripcion = info_vo.descripcion