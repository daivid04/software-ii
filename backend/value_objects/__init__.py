"""Value Objects del dominio"""
from .precio import Precio
from .stock import Stock
from .estado_pago import EstadoPago
from .garantia import Garantia
from .email import Email
from .especialidad import Especialidad
from .codigo_barras import CodigoBarra
from .estado import Estado

__all__ = [
    "Precio",
    "Stock",
    "EstadoPago",
    "Garantia",
    "Email",
    "Especialidad",
    "CodigoBarra",
    "Estado"
]
