from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import relationship
from db.base import Base
from src.ventas.domain.venta_domain import VentaDomain



class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, nullable=False)

    productos = relationship("VentaProducto", back_populates="venta")

    def to_domain(self) -> VentaDomain:
        return VentaDomain(
            id=self.id,
            fecha=self.fecha,
            productos=[{"producto_id": p.producto_id, "cantidad": p.cantidad} for p in self.productos]
        )

    def from_domain(self, domain: VentaDomain):
        self.fecha = domain.fecha
        # La gestión de los productos (detalles) la orquestará el Service