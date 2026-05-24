from dataclasses import dataclass, field
from datetime import datetime
from src.shared.domain.value_objects import CantidadVentaVO, FechaVentaVO

@dataclass
class VentaDomain:
    id: int = None
    fecha: datetime = None
    productos: list = field(default_factory=list)

    def inicializar_fecha(self, fecha_mecanica: datetime):
        fecha_vo = FechaVentaVO(fecha_mecanica)
        self.fecha = fecha_vo.valor

    def agregar_detalle(self, producto_id: int, cantidad: int):
        # Validamos con el VO
        cantidad_vo = CantidadVentaVO(cantidad)
        
        # Guardamos en la lista de dominio
        self.productos.append({
            "producto_id": producto_id,
            "cantidad": cantidad_vo.valor
        })