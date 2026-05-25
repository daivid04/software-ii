from sqlalchemy.orm import Session
from src.ordenes.infrastructure.orden import Orden
from sqlalchemy import Date, cast
from sqlalchemy.exc import IntegrityError

class OrdenRepository:
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, orden: Orden):
        """Persiste el Agregado completo (Orden + Servicios + Empleados) de forma atómica"""
        self.db.add(orden)
        self.db.commit()
        self.db.refresh(orden)
        return orden

    def listar_catalogo_ordenes(self):
        return self.db.query(Orden).all()

    def consultar_orden(self, id: int):
        return self.db.query(Orden).filter(Orden.id == id).first()

    def dar_de_baja_orden(self, id: int):
        orden = self.consultar_orden(id)
        if orden:
            try:
                self.db.delete(orden)
                self.db.commit()
            except IntegrityError:
                self.db.rollback()
                raise ValueError("No se puede eliminar la orden por restricciones de la base de datos")
            return True
        return False

    def consultar_ordenes_por_fecha(self, fecha):
        return self.db.query(Orden).filter(
            cast(Orden.fecha, Date) == fecha
        ).all()