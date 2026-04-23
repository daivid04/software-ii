import re
from typing import Final

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