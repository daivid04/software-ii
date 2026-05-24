from sqlalchemy import Column, Integer, String, Date
from db.base import Base
from sqlalchemy.orm import relationship
from db.models.value_objects import GarantiaVO, EstadoPagoVO, PrecioOrdenVO

class Orden(Base):
    __tablename__ = "ordenes"

    id = Column(Integer, primary_key=True)
    garantia = Column(Integer, nullable=False)
    estadoPago = Column(String, nullable=False)
    precio = Column(Integer, nullable=False)
    fecha = Column(Date, nullable=False)

    servicios = relationship("OrdenServicio", back_populates="orden")
    empleados = relationship("OrdenEmpleado", back_populates="orden")

    # ==========================================
    # LÓGICA DE DOMINIO 
    # ==========================================

    def inicializar_datos_basicos(self, garantia: int, estadoPago: str, precio: int, fecha):
        """Asigna los datos validando contra los Value Objects"""
        self.garantia = GarantiaVO(garantia).valor
        self.estadoPago = EstadoPagoVO(estadoPago).valor
        self.precio = PrecioOrdenVO(precio).valor
        self.fecha = fecha

    def agregar_servicio(self, servicio, precio_servicio: int, clase_orden_servicio):
        """La Orden orquesta la adición de un servicio validando su precio"""
        precio_vo = PrecioOrdenVO(precio_servicio)
        
        nuevo_detalle = clase_orden_servicio(
            servicio_id=servicio.id, 
            precio_servicio=precio_vo.valor
        )
        self.servicios.append(nuevo_detalle)

    def asignar_empleado(self, empleado, clase_orden_empleado):
        """La Orden asigna un empleado aplicando reglas de negocio"""
        if empleado.estado != "activo":
            raise ValueError(f"No se puede asignar la orden al empleado {empleado.nombres} porque no está activo")
            
        nueva_asignacion = clase_orden_empleado(empleado_id=empleado.id)
        self.empleados.append(nueva_asignacion)