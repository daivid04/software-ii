from sqlalchemy.orm import Session
from db.models import Empleado

from schemas.empleado_schema import EmpleadoCreate

class EmpleadoRepository:

    def __init__(self, db: Session):
        self.db = db
    
    def registrar_empleado(self, empleado_data: EmpleadoCreate):
        empleado = Empleado(**empleado_data.model_dump())
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

    def actualizar_empleado(self, id: int, empleado_data: EmpleadoCreate):
        empleado = self.consultar_empleado(id)
        if not empleado:
            return None
        data = empleado_data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(empleado, key, value)
        self.db.commit()
        self.db.refresh(empleado)
        return empleado
    
    def dar_de_baja_empleado(self, id: int):
        empleado = self.consultar_empleado(id)
        if empleado:
            self.db.delete(empleado)
            self.db.commit()
        return empleado