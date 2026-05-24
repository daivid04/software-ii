from dataclasses import dataclass
from src.producto.domain.producto_domain import ProductoDomain
from src.shared.domain.value_objects import CompatibilidadVehiculoVO

@dataclass
class AutoparteDomain(ProductoDomain):
    modelo: str
    anio: str

    def asignar_compatibilidad(self, modelo: str, anio: str):
        # Aquí usamos el VO de compatibilidad
        vo = CompatibilidadVehiculoVO(modelo=modelo, anio=anio)
        self.modelo = vo.modelo
        self.anio = vo.anio