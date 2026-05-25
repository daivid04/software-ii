from sqlalchemy import Column, Integer, String, Date
from db.base import Base
from sqlalchemy.orm import relationship
from src.ordenes.domain.orden_domain import OrdenDomain

class Orden(Base):
    __tablename__ = "ordenes"

    id = Column(Integer, primary_key=True)
    garantia = Column(Integer, nullable=False)
    estadoPago = Column(String, nullable=False)
    precio = Column(Integer, nullable=False)
    fecha = Column(Date, nullable=False)

    servicios = relationship("OrdenServicio", back_populates="orden")
    empleados = relationship("OrdenEmpleado", back_populates="orden")

    def to_domain(self) -> OrdenDomain:
        domain = OrdenDomain(
            id=self.id,
            garantia=self.garantia,
            estadoPago=self.estadoPago,
            precio=self.precio,
            fecha=self.fecha
        )
        for s in self.servicios:
            domain.servicios.append({"servicio_id": s.servicio_id, "precio_servicio": s.precio_servicio})
        for e in self.empleados:
            domain.empleados.append({"empleado_id": e.empleado_id})
        return domain

    def from_domain(self, domain: OrdenDomain):
        self.garantia = domain.garantia
        self.estadoPago = domain.estadoPago
        self.precio = domain.precio
        self.fecha = domain.fecha