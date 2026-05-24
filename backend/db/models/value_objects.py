import re
from dataclasses import dataclass

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