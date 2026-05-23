from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from repositories.venta_repo import VentaRepository
from schemas.venta_schema import VentaCreate



class VentaService:
    
    def __init__(self, db: Session):
        self.repo = VentaRepository(db)

    def registrar_nueva_venta(self, data: VentaCreate):
        """Registra una nueva venta en el sistema"""
        productos = getattr(data, "productos", None)
        if productos:
            productos_list = [p.model_dump() if hasattr(p, 'model_dump') else p for p in productos]
            try:
                return self.repo.registrar_venta_con_productos(data.fecha, productos_list)
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
        return self.repo.registrar_venta(data.fecha)

    def obtener_registro_completo_ventas(self):
        """Obtiene el registro completo de todas las ventas"""
        return self.repo.listar_registro_ventas()

    def consultar_venta(self, id: int):
        """Consulta una venta por su ID"""
        return self.repo.consultar_venta(id)

    def consultar_ventas_por_fecha(self, fecha: datetime):
        """Consulta ventas por una fecha específica"""
        return self.repo.consultar_ventas_por_fecha(fecha)

    def dar_de_baja_venta(self, id: int):
        """Da de baja una venta del sistema"""
        return self.repo.dar_de_baja_venta(id)
