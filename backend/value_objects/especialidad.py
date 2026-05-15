class Especialidad:
    """Value Object para especialidades de empleados"""
    
    ESPECIALIDADES_VALIDAS = {
        "mecanica",
        "electricidad",
        "suspension",
        "sistemas",
        "chapa",
        "pintura",
        "tapiceria",
        "transmision"
    }
    
    def __init__(self, nombre: str):
        if not isinstance(nombre, str):
            raise TypeError("Especialidad debe ser una cadena")
        nombre = nombre.strip().lower()
        if nombre not in self.ESPECIALIDADES_VALIDAS:
            raise ValueError(
                f"Especialidad inválida. Válidas: {self.ESPECIALIDADES_VALIDAS}"
            )
        self._nombre = nombre
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def es_mecanica(self) -> bool:
        return self._nombre == "mecanica"
    
    @property
    def es_electricidad(self) -> bool:
        return self._nombre == "electricidad"
    
    @property
    def es_sistemas(self) -> bool:
        return self._nombre == "sistemas"
    
    def __eq__(self, otro):
        if not isinstance(otro, Especialidad):
            return False
        return self._nombre == otro._nombre
    
    def __hash__(self):
        return hash(self._nombre)
    
    def __repr__(self):
        return f"Especialidad({self._nombre})"
