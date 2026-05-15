from sqlalchemy import Column, Integer, String, Date
from db.base import Base
from sqlalchemy.orm import relationship
from core.value_objects import Precio, EstadoPago, Garantia


class Orden(Base):
    __tablename__ = "ordenes"

    id = Column(Integer, primary_key=True)
    garantia = Column(Integer, nullable=False)
    estadoPago = Column(String, nullable=False)
    precio = Column(Integer, nullable=False)
    fecha = Column(Date, nullable=False)

    servicios = relationship("OrdenServicio", back_populates="orden", cascade="all, delete-orphan")
    empleados = relationship("OrdenEmpleado", back_populates="orden", cascade="all, delete-orphan")

    def __init__(self, garantia: int, estadoPago: str, precio: float, fecha):
        # Validar using Value Objects
        self._garantia_vo = Garantia(garantia)
        self._estado_pago_vo = EstadoPago(estadoPago)
        self._precio_vo = Precio(precio)
        
        # Asignar valores validados
        self.garantia = self._garantia_vo.value
        self.estadoPago = self._estado_pago_vo.value
        self.precio = self._precio_vo.value
        self.fecha = fecha

    def cambiar_estado_pago(self, nuevo_estado: str) -> None:
        estado_vo = EstadoPago(nuevo_estado)
        self.estadoPago = estado_vo.value

    def agregar_servicio(self, orden_servicio: 'OrdenServicio') -> None:
        # Validar el precio del servicio
        precio_vo = Precio(float(orden_servicio.precio_servicio))
        
        # Agregar a la lista de servicios
        self.servicios.append(orden_servicio)
        
        # Actualizar el total (invariante)
        self.precio += precio_vo.value

    def asignar_empleado(self, orden_empleado: 'OrdenEmpleado') -> None:

        self.empleados.append(orden_empleado)

    def obtener_precio_total(self) -> float:
        """Retorna el precio total de la orden."""
        return self.precio

    def obtener_estado_pago(self) -> str:
        """Retorna el estado de pago actual."""
        return self.estadoPago

    def obtener_garantia(self) -> int:
        """Retorna la garantía en años."""
        return self.garantia