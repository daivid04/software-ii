class Garantia:
    """Value Object para períodos de garantía"""
    
    RANGO_VALIDO = (0, 10)  # Años
    
    def __init__(self, anos: int):
        if not isinstance(anos, int):
            raise TypeError("Garantía debe ser un entero")
        if anos < self.RANGO_VALIDO[0] or anos > self.RANGO_VALIDO[1]:
            raise ValueError(
                f"Garantía debe estar entre {self.RANGO_VALIDO[0]} y {self.RANGO_VALIDO[1]} años"
            )
        self._anos = anos
    
    @property
    def anos(self) -> int:
        return self._anos
    
    @property
    def meses(self) -> int:
        return self._anos * 12
    
    @property
    def dias(self) -> int:
        return self._anos * 365
    
    @property
    def es_sin_garantia(self) -> bool:
        return self._anos == 0
    
    @property
    def es_extendida(self) -> bool:
        return self._anos >= 5
    
    def __eq__(self, otro):
        if not isinstance(otro, Garantia):
            return False
        return self._anos == otro._anos
    
    def __lt__(self, otro):
        if not isinstance(otro, Garantia):
            return NotImplemented
        return self._anos < otro._anos
    
    def __le__(self, otro):
        if not isinstance(otro, Garantia):
            return NotImplemented
        return self._anos <= otro._anos
    
    def __gt__(self, otro):
        if not isinstance(otro, Garantia):
            return NotImplemented
        return self._anos > otro._anos
    
    def __ge__(self, otro):
        if not isinstance(otro, Garantia):
            return NotImplemented
        return self._anos >= otro._anos
    
    def __repr__(self):
        return f"Garantia({self._anos} años)"
