from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from repositories.venta_repo import VentaRepository
from schemas.venta_schema import VentaCreate



class VentaService:
    
    def __init__(self, db: Session):
        self.repo = VentaRepository(db)

    def create_venta(self, data: VentaCreate):
        productos = getattr(data, "productos", None)
        if productos:
            productos_list = [p.model_dump() if hasattr(p, 'model_dump') else p for p in productos]
            try:
                return self.repo.create_with_products(data.fecha, productos_list)
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
        return self.repo.create(data.fecha)

    def list_ventas(self):
        return self.repo.get_all()

    def get_by_id(self, id: int):
        return self.repo.get_by_id(id)

    def get_by_fecha(self, fecha: datetime):
        return self.repo.get_by_fecha(fecha)

    def delete_venta(self, id: int):
        return self.repo.delete(id)
