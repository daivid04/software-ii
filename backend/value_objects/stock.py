class Stock:
    """Value Object para niveles de stock"""
    
    def __init__(self, cantidad: int, stock_minimo: int = 0):
        if not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError("Stock debe ser un entero no negativo")
        if not isinstance(stock_minimo, int) or stock_minimo < 0:
            raise ValueError("Stock mínimo debe ser un entero no negativo")
        self._cantidad = cantidad
        self._stock_minimo = stock_minimo
    
    @property
    def cantidad(self) -> int:
        return self._cantidad
    
    @property
    def stock_minimo(self) -> int:
        return self._stock_minimo
    
    def esta_bajo(self) -> bool:
        """Verifica si el stock está por debajo del mínimo"""
        return self._cantidad < self._stock_minimo
    
    def es_disponible(self, cantidad_requerida: int) -> bool:
        """Verifica si hay suficiente stock disponible"""
        if not isinstance(cantidad_requerida, int) or cantidad_requerida < 0:
            raise ValueError("Cantidad debe ser un entero no negativo")
        return self._cantidad >= cantidad_requerida
    
    def reducir(self, cantidad: int) -> 'Stock':
        """Retorna nuevo Stock con cantidad reducida"""
        if not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError("Cantidad a reducir debe ser un entero no negativo")
        if cantidad > self._cantidad:
            raise ValueError(f"No hay suficiente stock. Disponible: {self._cantidad}, Solicitado: {cantidad}")
        return Stock(self._cantidad - cantidad, self._stock_minimo)
    
    def incrementar(self, cantidad: int) -> 'Stock':
        """Retorna nuevo Stock con cantidad incrementada"""
        if not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError("Cantidad a incrementar debe ser un entero no negativo")
        return Stock(self._cantidad + cantidad, self._stock_minimo)
    
    def __eq__(self, otro):
        if not isinstance(otro, Stock):
            return False
        return self._cantidad == otro._cantidad and self._stock_minimo == otro._stock_minimo
    
    def __repr__(self):
        return f"Stock(cantidad={self._cantidad}, mínimo={self._stock_minimo})"
