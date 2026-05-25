from dataclasses import dataclass
from src.shared.domain.value_objects import InformacionEmpleadoVO, EstadoEmpleadoVO

@dataclass
class EmpleadoDomain:
    id: int | None = None
    nombres: str = ""
    apellidos: str = ""
    estado: str = "activo"
    especialidad: str = ""

    def actualizar_informacion(self, nombres: str, apellidos: str, especialidad: str):
        info_vo = InformacionEmpleadoVO(nombres=nombres, apellidos=apellidos, especialidad=especialidad)
        self.nombres = info_vo.nombres
        self.apellidos = info_vo.apellidos
        self.especialidad = info_vo.especialidad

    def cambiar_estado(self, estado: str):
        estado_vo = EstadoEmpleadoVO(valor=estado)
        self.estado = estado_vo.valor.lower()