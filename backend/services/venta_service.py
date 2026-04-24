from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from repositories.venta_repo import VentaRepository
from schemas.venta_schema import VentaCreate
from core.value_objects import Cantidad, CantidadProductos


class VentaService:

    def __init__(self, db: Session):
        self.repo = VentaRepository(db)

    def create_venta(self, data: VentaCreate):

        try:
            productos = getattr(data, "productos", None)
            if productos:
                productos_list = [p.model_dump() if hasattr(p, 'model_dump') else p for p in productos]
                try:
                    return self.repo.create_with_products(data.fecha, productos_list)
                except ValueError as e:
                    raise HTTPException(status_code=400, detail=str(e))
            return self.repo.create(data.fecha)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def list_ventas(self):
        """Obtiene todas las ventas."""
        return self.repo.get_all()

    def get_by_id(self, id: int):
        """Obtiene una venta por ID."""
        return self.repo.get_by_id(id)

    def get_by_fecha(self, fecha: datetime):
        """Obtiene ventas por fecha."""
        return self.repo.get_by_fecha(fecha)

    def delete_venta(self, id: int):
        """Elimina una venta."""
        return self.repo.delete(id)

    def obtener_total_venta(self, id: int) -> float:

        venta = self.repo.get_by_id(id)
        if not venta:
            raise HTTPException(status_code=404, detail="Venta no encontrada")
        
        return venta.calcular_total()

    def obtener_resumen_venta(self, id: int) -> dict:

        venta = self.repo.get_by_id(id)
        if not venta:
            raise HTTPException(status_code=404, detail="Venta no encontrada")
        
        return {
            "id": venta.id,
            "fecha": venta.obtener_fecha(),
            "cantidad_productos": venta.obtener_cantidad_productos(),
            "cantidad_items_totales": venta.obtener_cantidad_total_items(),
            "total": venta.calcular_total(),
            "tiene_productos": venta.tiene_productos()
        }
