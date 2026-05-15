import re

class Email:
    """Value Object para direcciones de email"""
    
    PATRON_EMAIL = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    def __init__(self, direccion: str):
        if not isinstance(direccion, str):
            raise TypeError("Email debe ser una cadena")
        direccion = direccion.strip().lower()
        if not re.match(self.PATRON_EMAIL, direccion):
            raise ValueError(f"Email inválido: {direccion}")
        self._direccion = direccion
    
    @property
    def direccion(self) -> str:
        return self._direccion
    
    @property
    def dominio(self) -> str:
        return self._direccion.split('@')[1]
    
    @property
    def usuario(self) -> str:
        return self._direccion.split('@')[0]
    
    def __eq__(self, otro):
        if not isinstance(otro, Email):
            return False
        return self._direccion == otro._direccion
    
    def __hash__(self):
        return hash(self._direccion)
    
    def __repr__(self):
        return f"Email({self._direccion})"
    
    def __str__(self):
        return self._direccion
