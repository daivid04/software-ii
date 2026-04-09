from sqlalchemy.orm import Session
from db.models import Empleado

from schemas.empleado_schema import EmpleadoCreate

class EmpleadoRepository:

    def __init__(self, db: Session):
        self.db = db
    
    def create(self, empleado_data: EmpleadoCreate):
        empleado = Empleado(**empleado_data.model_dump())
        self.db.add(empleado)
        self.db.commit()
        self.db.refresh(empleado)
        return empleado

    def get_all(self):
        return self.db.query(Empleado).all()
    
    def get_by_id(self, id: int):
        return self.db.query(Empleado).filter(Empleado.id == id).first()

    def get_by_name(self, nombres: str):
        return self.db.query(Empleado).filter(Empleado.nombres == nombres).first()

    def update(self, id: int, empleado_data: EmpleadoCreate):
        empleado = self.get_by_id(id)
        if not empleado:
            return None
        data = empleado_data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(empleado, key, value)
        self.db.commit()
        self.db.refresh(empleado)
        return empleado
    
    def delete(self, id: int):
        empleado = self.get_by_id(id)
        if empleado:
            self.db.delete(empleado)
            self.db.commit()
        return empleado