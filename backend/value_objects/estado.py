class Estado:
    """Value Object para estados de empleados"""
    
    ESTADOS_VALIDOS = {"activo", "inactivo", "licencia", "suspendido"}
    
    def __init__(self, nombre: str):
        if not isinstance(nombre, str):
            raise TypeError("Estado debe ser una cadena")
        nombre = nombre.strip().lower()
        if nombre not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido. Válidos: {self.ESTADOS_VALIDOS}")
        self._nombre = nombre
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def es_activo(self) -> bool:
        return self._nombre == "activo"
    
    @property
    def es_inactivo(self) -> bool:
        return self._nombre == "inactivo"
    
    @property
    def puede_trabajar(self) -> bool:
        return self._nombre in {"activo", "licencia"}
    
    def cambiar_a(self, nuevo_estado: str) -> 'Estado':
        """Retorna nuevo Estado"""
        return Estado(nuevo_estado)
    
    def __eq__(self, otro):
        if not isinstance(otro, Estado):
            return False
        return self._nombre == otro._nombre
    
    def __repr__(self):
        return f"Estado({self._nombre})"
