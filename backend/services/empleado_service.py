from sqlalchemy.orm import Session
from repositories.empleado_repo import EmpleadoRepository
from schemas.empleado_schema import EmpleadoCreate

class EmpleadoService:

    def __init__(self, db: Session):
        self.repo = EmpleadoRepository(db)
    
    def create_empleado(self, data: EmpleadoCreate):
        # schema uses 'nombres' (plural) so check that field
        if self.repo.get_by_name(data.nombres):
            raise ValueError("Ya existe un empleado con ese nombre")
        empleado_data = data
        empleado = self.repo.create(empleado_data)
        return empleado
    
    def list_empleados(self):
        return self.repo.get_all()
    
    def get_by_id(self, id: int):
        return self.repo.get_by_id(id)

    def update_empleado(self, id: int, data: EmpleadoCreate):
        return self.repo.update(id, data)
    
    def delete_empleado(self, id: int):
        return self.repo.delete(id)