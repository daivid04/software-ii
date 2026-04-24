import re
from typing import Final
from enum import Enum

class Email:
    def __init__(self, value: str):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Email inválido")
        self._value: Final[str] = value

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other) -> bool:
        return isinstance(other, Email) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)


class Precio:
    def __init__(self, value: float):
        if value <= 0:
            raise ValueError("Precio debe ser mayor a 0")
        self._value: Final[float] = value

    @property
    def value(self) -> float:
        return self._value

    def __eq__(self, other) -> bool:
        return isinstance(other, Precio) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)


class EstadoPago:
    """Value Object para representar el estado de pago de una orden."""
    
    ESTADOS_VALIDOS = {"pendiente", "parcial", "completado"}
    
    def __init__(self, value: str):
        if value.lower() not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado de pago inválido. Debe ser uno de: {', '.join(self.ESTADOS_VALIDOS)}")
        self._value: Final[str] = value.lower()

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other) -> bool:
        return isinstance(other, EstadoPago) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __repr__(self) -> str:
        return f"EstadoPago({self._value})"


class Garantia:
    """Value Object para representar la garantía (en años) de una orden de servicio."""
    
    def __init__(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Garantía debe ser un número entero no negativo")
        if value > 10:
            raise ValueError("Garantía no puede exceder 10 años")
        self._value: Final[int] = value

    @property
    def value(self) -> int:
        return self._value

    def __eq__(self, other) -> bool:
        return isinstance(other, Garantia) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __repr__(self) -> str:
        return f"Garantia({self._value} años)"

    def es_valida(self) -> bool:
        """Verifica si la garantía sigue siendo válida (simplemente si es > 0)."""
        return self._value > 0


class Cantidad:
    """Value Object para representar cantidad de productos."""
    
    def __init__(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Cantidad debe ser un número entero mayor a 0")
        if value > 10000:
            raise ValueError("Cantidad no puede exceder 10000 unidades")
        self._value: Final[int] = value

    @property
    def value(self) -> int:
        return self._value

    def __eq__(self, other) -> bool:
        return isinstance(other, Cantidad) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __repr__(self) -> str:
        return f"Cantidad({self._value})"


class CantidadProductos:
    """Value Object para representar la cantidad de productos diferentes en una venta."""
    
    def __init__(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Cantidad de productos debe ser un número entero no negativo")
        self._value: Final[int] = value

    @property
    def value(self) -> int:
        return self._value

    def __eq__(self, other) -> bool:
        return isinstance(other, CantidadProductos) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __repr__(self) -> str:
        return f"CantidadProductos({self._value})"

    def es_vacia(self) -> bool:
        """Verifica si la venta no tiene productos."""
        return self._value == 0