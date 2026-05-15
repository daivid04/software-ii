class EstadoPago:
    """Value Object para estados de pago"""
    
    ESTADOS_VALIDOS = {"pendiente", "parcial", "completado"}
    TRANSICIONES_VALIDAS = {
        "pendiente": {"parcial", "completado"},
        "parcial": {"completado"},
        "completado": set()
    }
    
    def __init__(self, estado: str):
        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido. Válidos: {self.ESTADOS_VALIDOS}")
        self._estado = estado
    
    @property
    def estado(self) -> str:
        return self._estado
    
    def puede_transicionar_a(self, nuevo_estado: str) -> bool:
        """Verifica si la transición es válida"""
        if nuevo_estado not in self.ESTADOS_VALIDOS:
            return False
        return nuevo_estado in self.TRANSICIONES_VALIDAS.get(self._estado, set())
    
    def transicionar_a(self, nuevo_estado: str) -> 'EstadoPago':
        """Retorna nuevo EstadoPago con el nuevo estado"""
        if not self.puede_transicionar_a(nuevo_estado):
            raise ValueError(
                f"Transición inválida: {self._estado} → {nuevo_estado}"
            )
        return EstadoPago(nuevo_estado)
    
    @property
    def es_completado(self) -> bool:
        return self._estado == "completado"
    
    @property
    def es_pendiente(self) -> bool:
        return self._estado == "pendiente"
    
    @property
    def es_parcial(self) -> bool:
        return self._estado == "parcial"
    
    def __eq__(self, otro):
        if not isinstance(otro, EstadoPago):
            return False
        return self._estado == otro._estado
    
    def __repr__(self):
        return f"EstadoPago({self._estado})"
