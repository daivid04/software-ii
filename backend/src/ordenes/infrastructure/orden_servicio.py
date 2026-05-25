from sqlalchemy import Column, Integer, ForeignKey
from db.base import Base
from sqlalchemy.orm import relationship

class OrdenServicio(Base):
    __tablename__ = "orden_servicio"

    id = Column(Integer, primary_key=True)
    orden_id = Column(Integer, ForeignKey("ordenes.id"), nullable=False)
    servicio_id = Column(Integer, ForeignKey("servicios.id"), nullable=False)
    precio_servicio = Column(Integer, nullable=False)

    servicio = relationship("Servicio", back_populates="ordenes")
    orden = relationship("Orden", back_populates="servicios")