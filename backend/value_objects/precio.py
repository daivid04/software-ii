class Precio:
    """Value Object para precios"""
    
    def __init__(self, valor: float):
        if not isinstance(valor, (int, float)):
            raise TypeError("Precio debe ser numérico")
        if valor < 0:
            raise ValueError("Precio no puede ser negativo")
        if valor == 0:
            raise ValueError("Precio debe ser mayor a 0")
        self._valor = float(valor)
    
    @property
    def valor(self) -> float:
        return self._valor
    
    def __eq__(self, otro):
        if not isinstance(otro, Precio):
            return False
        return self._valor == otro._valor
    
    def __lt__(self, otro):
        if not isinstance(otro, Precio):
            return NotImplemented
        return self._valor < otro._valor
    
    def __le__(self, otro):
        if not isinstance(otro, Precio):
            return NotImplemented
        return self._valor <= otro._valor
    
    def __gt__(self, otro):
        if not isinstance(otro, Precio):
            return NotImplemented
        return self._valor > otro._valor
    
    def __ge__(self, otro):
        if not isinstance(otro, Precio):
            return NotImplemented
        return self._valor >= otro._valor
    
    def __add__(self, otro):
        if not isinstance(otro, Precio):
            return NotImplemented
        return Precio(self._valor + otro._valor)
    
    def __sub__(self, otro):
        if not isinstance(otro, Precio):
            return NotImplemented
        resultado = self._valor - otro._valor
        return Precio(resultado) if resultado > 0 else Precio(0.01)
    
    def __mul__(self, factor: float):
        if not isinstance(factor, (int, float)):
            return NotImplemented
        return Precio(self._valor * factor)
    
    def __repr__(self):
        return f"Precio({self._valor})"
    
    def __str__(self):
        return f"${self._valor:.2f}"
