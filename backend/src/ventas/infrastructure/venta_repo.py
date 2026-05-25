from sqlalchemy import Date, cast
from sqlalchemy.orm import Session
from datetime import datetime
from src.ventas.infrastructure.venta import Venta




class VentaRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def guardar(self, venta: Venta):
        """Persiste el Agregado completo (Venta + Detalles) en la base de datos"""
        self.db.add(venta)
        self.db.commit()
        self.db.refresh(venta)
        return venta

    def listar_registro_ventas(self):
        """Lista todas las ventas registradas"""
        return self.db.query(Venta).all()

    def consultar_venta(self, id: int):
        """Consulta una venta por su ID"""
        return self.db.query(Venta).filter(Venta.id == id).first()

    def dar_de_baja_venta(self, id: int):
        """Da de baja una venta del sistema"""
        venta = self.consultar_venta(id)
        if venta:
            self.db.delete(venta)
            self.db.commit()
            return True
        return False

    def consultar_ventas_por_fecha(self, fecha: datetime):
        """Consulta ventas por fecha específica"""
        return self.db.query(Venta).filter(
            cast(Venta.fecha, Date) == fecha.date()
        ).all()
