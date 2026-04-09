from pydantic import BaseModel
from datetime import date
from schemas.servicio_schema import ServicioResponse
from schemas.empleado_schema import EmpleadoResponse

class OrdenBase(BaseModel):
    garantia: int
    estadoPago: str
    precio: int
    fecha: date


class OrdenServicioBase(BaseModel):
    servicio_id: int
    precio_servicio: int

class OrdenServicioResponse(OrdenServicioBase):
    servicio: ServicioResponse | None = None
    class Config:
        from_attributes = True


class OrdenEmpleadoBase(BaseModel):
    empleado_id: int

class OrdenEmpleadoResponse(OrdenEmpleadoBase):
    empleado: EmpleadoResponse | None = None
    class Config:
        from_attributes = True


class OrdenCreate(OrdenBase):
    servicios: list[OrdenServicioBase] | None = []
    empleados: list[OrdenEmpleadoBase] | None = []

class OrdenResponse(OrdenBase):
    id: int
    servicios: list[OrdenServicioResponse] | None = None
    empleados: list[OrdenEmpleadoResponse] | None = None

    class Config:
        from_attributes = True