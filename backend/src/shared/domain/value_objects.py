import re
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class PrecioVO:
    """Value Object para manejar reglas de precios"""
    compra: float
    venta: float

    def __post_init__(self):
        if self.compra < 0 or self.venta < 0:
            raise ValueError("Los precios no pueden ser negativos")
        if self.venta <= self.compra:
            raise ValueError("El precio de venta debe ser mayor al precio de compra")

@dataclass(frozen=True)
class InventarioVO:
    """Value Object para manejar reglas de stock"""
    stock_actual: int
    stock_minimo: int

    def __post_init__(self):
        if self.stock_actual < 0 or self.stock_minimo < 0:
            raise ValueError("El stock no puede ser negativo")

    def despachar(self, cantidad: int) -> 'InventarioVO':
        if cantidad <= 0:
            raise ValueError("La cantidad a despachar debe ser mayor a 0")
        if self.stock_actual - cantidad < 0:
            raise ValueError("Stock insuficiente para despachar")
        return InventarioVO(self.stock_actual - cantidad, self.stock_minimo)
    
@dataclass(frozen=True)
class CompatibilidadVehiculoVO:
    """Value Object para manejar las reglas de compatibilidad de una autoparte"""
    modelo: str
    anio: str

    def __post_init__(self):
        if not self.modelo or len(self.modelo.strip()) < 2:
            raise ValueError("El modelo del vehículo debe tener al menos 2 caracteres")
        
        # Validamos que el string de 'año' contenga al menos un año válido de 4 dígitos
        if not self.anio or not re.search(r'\d{4}', self.anio):
            raise ValueError("El año de compatibilidad debe contener al menos un año válido (ej. 2020, 2018-2023)")
        
@dataclass(frozen=True)
class CantidadVentaVO:
    """Value Object para asegurar que la cantidad de un ítem vendido sea válida"""
    valor: int

    def __post_init__(self):
        if self.valor <= 0:
            raise ValueError("La cantidad de productos en la venta debe ser mayor a cero")

@dataclass(frozen=True)
class FechaVentaVO:
    """Value Object para validar que la fecha de la transacción sea coherente"""
    valor: datetime

    def __post_init__(self):
        # Regla de negocio: No se pueden registrar ventas con fechas del futuro
        ahora = datetime.now(timezone.utc)
        
        fecha_a_comparar = self.valor
        if fecha_a_comparar.tzinfo is None:
            # Si viene sin zona horaria, le ponemos UTC por defecto
            fecha_a_comparar = fecha_a_comparar.replace(tzinfo=timezone.utc)
        else:
            # Si ya trae zona horaria, la normalizamos a UTC
            fecha_a_comparar = fecha_a_comparar.astimezone(timezone.utc)
            
        if fecha_a_comparar > ahora:
            raise ValueError("La fecha de la venta no puede ser una fecha futura")
        
@dataclass(frozen=True)
class InformacionServicioVO:
    """Value Object para validar la información de un servicio mecánico"""
    nombre: str
    descripcion: str

    def __post_init__(self):
        if not self.nombre or len(self.nombre.strip()) < 3:
            raise ValueError("El nombre del servicio debe tener al menos 3 caracteres")
        if not self.descripcion or len(self.descripcion.strip()) < 10:
            raise ValueError("La descripción del servicio debe tener al menos 10 caracteres")
        
@dataclass(frozen=True)
class InformacionEmpleadoVO:
    """Value Object para asegurar la validez de los datos de un empleado"""
    nombres: str
    apellidos: str
    especialidad: str

    def __post_init__(self):
        if not self.nombres or len(self.nombres.strip()) < 2:
            raise ValueError("Los nombres deben tener al menos 2 caracteres")
        if not self.apellidos or len(self.apellidos.strip()) < 2:
            raise ValueError("Los apellidos deben tener al menos 2 caracteres")
        if not self.especialidad or len(self.especialidad.strip()) < 2:
            raise ValueError("La especialidad debe tener al menos 2 caracteres")

@dataclass(frozen=True)
class EstadoEmpleadoVO:
    """Value Object para garantizar que el estado del empleado sea coherente"""
    valor: str

    def __post_init__(self):
        estados_validos = ["activo", "inactivo", "vacaciones", "suspendido"]
        if not self.valor or self.valor.lower() not in estados_validos:
            raise ValueError(f"Estado de empleado no válido. Debe ser uno de: {', '.join(estados_validos)}")
        
@dataclass(frozen=True)
class GarantiaVO:
    """Valida que los meses/días de garantía no sean negativos"""
    valor: int
    def __post_init__(self):
        if self.valor < 0:
            raise ValueError("La garantía no puede ser un valor negativo")

@dataclass(frozen=True)
class EstadoPagoVO:
    """Garantiza que el estado de pago pertenezca a un glosario cerrado"""
    valor: str
    def __post_init__(self):
        estados_permitidos = ["pendiente", "pagado", "parcial", "cancelado"]
        if not self.valor or self.valor.lower() not in estados_permitidos:
            raise ValueError(f"Estado de pago inválido. Permitidos: {', '.join(estados_permitidos)}")

@dataclass(frozen=True)
class PrecioOrdenVO:
    """Valida que los precios y cobros en la orden no sean negativos"""
    valor: int
    def __post_init__(self):
        if self.valor < 0:
            raise ValueError("El precio no puede ser negativo")