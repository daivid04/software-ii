from pydantic import BaseModel
from pydantic import ConfigDict

class EmpleadoBase(BaseModel):
    nombres: str
    apellidos: str
    estado: str
    especialidad: str

class EmpleadoCreate(EmpleadoBase):
    pass

class EmpleadoResponse(EmpleadoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)