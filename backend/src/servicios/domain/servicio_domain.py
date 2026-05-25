from dataclasses import dataclass
from src.shared.domain.value_objects import InformacionServicioVO

@dataclass
class ServicioDomain:
    id: int | None = None
    nombre: str = ""
    descripcion: str = ""

    def actualizar_informacion(self, nombre: str, descripcion: str):
        # El Value Object se encarga de las validaciones y sanitización
        info_vo = InformacionServicioVO(nombre=nombre, descripcion=descripcion)
        self.nombre = info_vo.nombre
        self.descripcion = info_vo.descripcion