from pydantic import BaseModel, field_validator
from pydantic import ConfigDict
import re

class ServicioBase(BaseModel):
    nombre: str
    descripcion: str
    
    @field_validator('nombre', 'descripcion')
    @classmethod
    def sanitize_html(cls, v: str) -> str:
        """Prevenir inyección de scripts HTML/JavaScript"""
        if v is None:
            return v
        # Eliminar tags HTML y scripts
        v = re.sub(r'<[^>]*>', '', v)
        # Eliminar caracteres peligrosos
        v = re.sub(r'[<>"\']', '', v)
        return v.strip()


class ServicioCreate(ServicioBase):
    pass


class ServicioResponse(ServicioBase):
    id: int

    model_config = ConfigDict(from_attributes=True)