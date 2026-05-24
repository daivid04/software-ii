from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.models.empleado import Empleado
from schemas.empleado_schema import EmpleadoCreate

class EmpleadoRepository:

    def __init__(self, db: Session):
        self.db = db

    def guardar(self, empleado: Empleado):
        """Persiste el Agregado completo (inserción o actualización)"""
        self.db.add(empleado)
        self.db.commit()
        self.db.refresh(empleado)
        return empleado
    
    def listar_catalogo_empleados(self):
        return self.db.query(Empleado).all()
    
    def consultar_empleado(self, id: int):
        return self.db.query(Empleado).filter(Empleado.id == id).first()

    def buscar_empleado_por_nombre(self, nombres: str):
        return self.db.query(Empleado).filter(Empleado.nombres == nombres).first()

    def dar_de_baja_empleado(self, id: int):
        empleado = self.consultar_empleado(id)
        if empleado:
            try:
                self.db.delete(empleado)
                self.db.commit()
            except IntegrityError:
                self.db.rollback()
                raise ValueError("No se puede eliminar el empleado porque tiene órdenes de trabajo asociadas")
        return empleado