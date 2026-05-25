from dataclasses import dataclass, field
from datetime import date
from src.shared.domain.value_objects import GarantiaVO, EstadoPagoVO, PrecioOrdenVO

@dataclass
class OrdenDomain:
    id: int | None = None
    garantia: int = 0
    estadoPago: str = ""
    precio: int = 0
    fecha: date | None = None
    servicios: list = field(default_factory=list)
    empleados: list = field(default_factory=list)

    def inicializar_datos_basicos(self, garantia: int, estadoPago: str, precio: int, fecha: date):
        self.garantia = GarantiaVO(garantia).valor
        self.estadoPago = EstadoPagoVO(estadoPago).valor
        self.precio = PrecioOrdenVO(precio).valor
        self.fecha = fecha

    def agregar_servicio(self, servicio_id: int, precio_servicio: int):
        precio_vo = PrecioOrdenVO(precio_servicio)
        self.servicios.append({
            "servicio_id": servicio_id,
            "precio_servicio": precio_vo.valor
        })

    def asignar_empleado(self, empleado_id: int, estado_empleado: str, nombre_empleado: str):
        if estado_empleado != "activo":
            raise ValueError(f"No se puede asignar la orden al empleado {nombre_empleado} porque no está activo")
        
        self.empleados.append({
            "empleado_id": empleado_id
        })