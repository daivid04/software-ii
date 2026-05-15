class Cantidad:
    """Value Object para cantidades en rango comercial [1, 10000]"""
    
    MINIMO = 1
    MAXIMO = 10000
    
    def __init__(self, valor: int):
        if not isinstance(valor, int):
            raise TypeError("Cantidad debe ser un entero")
        if valor < self.MINIMO:
            raise ValueError(f"Cantidad debe ser >= {self.MINIMO}")
        if valor > self.MAXIMO:
            raise ValueError(f"Cantidad no puede exceder {self.MAXIMO}")
        self._valor = valor
    
    @property
    def valor(self) -> int:
        return self._valor
    
    def incrementar(self, cantidad: int) -> 'Cantidad':
        """Retorna nueva Cantidad incrementada"""
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("Cantidad a incrementar debe ser > 0")
        return Cantidad(self._valor + cantidad)
    
    def decrementar(self, cantidad: int) -> 'Cantidad':
        """Retorna nueva Cantidad decrementada"""
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("Cantidad a decrementar debe ser > 0")
        resultado = self._valor - cantidad
        return Cantidad(resultado)
    
    def es_minima(self) -> bool:
        """Verifica si es la cantidad mínima permitida"""
        return self._valor == self.MINIMO
    
    def es_maxima(self) -> bool:
        """Verifica si es la cantidad máxima permitida"""
        return self._valor == self.MAXIMO
    
    def __eq__(self, otro):
        if not isinstance(otro, Cantidad):
            return False
        return self._valor == otro._valor
    
    def __lt__(self, otro):
        if not isinstance(otro, Cantidad):
            return NotImplemented
        return self._valor < otro._valor
    
    def __le__(self, otro):
        if not isinstance(otro, Cantidad):
            return NotImplemented
        return self._valor <= otro._valor
    
    def __gt__(self, otro):
        if not isinstance(otro, Cantidad):
            return NotImplemented
        return self._valor > otro._valor
    
    def __ge__(self, otro):
        if not isinstance(otro, Cantidad):
            return NotImplemented
        return self._valor >= otro._valor
    
    def __repr__(self):
        return f"Cantidad({self._valor})"
    
    def __str__(self):
        return str(self._valor)
