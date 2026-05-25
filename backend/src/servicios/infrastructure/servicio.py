from sqlalchemy import Column, Integer, String
from src.servicios.domain.servicio_domain import ServicioDomain
from db.base import Base
from sqlalchemy.orm import relationship
from src.shared.domain.value_objects import InformacionServicioVO

class Servicio(Base):
    __tablename__ = "servicios"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False, unique=True)
    descripcion = Column(String, nullable=False, default="")

    ordenes = relationship("OrdenServicio", back_populates="servicio")



    def to_domain(self) -> ServicioDomain:
        """Convierte el modelo de BD a modelo de Dominio"""
        return ServicioDomain(
            id=self.id,
            nombre=self.nombre,
            descripcion=self.descripcion
        )

    def from_domain(self, domain: ServicioDomain):
        """Sincroniza los cambios del Dominio a la BD"""
        self.nombre = domain.nombre
        self.descripcion = domain.descripcion