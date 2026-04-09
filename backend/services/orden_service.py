from sqlalchemy.orm import Session
from repositories.orden_repo import OrdenRepository
from schemas.orden_schema import OrdenCreate
from fastapi import HTTPException

class OrdenService:
    
    def __init__(self, db: Session):
        self.repo = OrdenRepository(db)

    def create_orden(self, data: OrdenCreate):
        servicios = getattr(data, "servicios", None)
        empleados = getattr(data, "empleados", None)

        servicios_list = [p.model_dump() if hasattr(p, 'model_dump') else p for p in servicios] if servicios else []
        empleados_list = [p.model_dump() if hasattr(p, 'model_dump') else p for p in empleados] if empleados else []

        # Si hay servicios o empleados asociados, crear con relaciones
        if servicios_list or empleados_list:
            try:
                return self.repo.create_with_services(
                    data.garantia,
                    data.estadoPago,
                    data.precio,
                    data.fecha,
                    servicios_list,
                    empleados_list,
                )
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))

        # Caso simple: solo la orden
        return self.repo.create(data.garantia, data.estadoPago, data.precio, data.fecha)

    def list_ordens(self):
        return self.repo.get_all()

    def get_by_id(self, id: int):
        return self.repo.get_by_id(id)

    def get_by_fecha(self, fecha):
        return self.repo.get_by_fecha(fecha)

    def delete_orden(self, id: int):
        return self.repo.delete(id)