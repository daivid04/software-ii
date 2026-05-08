"""
Adaptador Secundario (Driven Adapter)
Implementa el Puerto Secundario (EmployeeRepository) usando SQLAlchemy
"""
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from db.models import Empleado
from hexagonal.ports.employee_driven_port import EmployeeRepository

class SqlAlchemyEmployeeRepository(EmployeeRepository):
    """Implementa el repositorio de empleados usando SQLAlchemy"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, employee_data: Dict) -> Dict:
        """Crear un empleado en la BD"""
        empleado = Empleado(**employee_data)
        self.db.add(empleado)
        self.db.commit()
        self.db.refresh(empleado)
        return self._to_dict(empleado)
    
    def get_all(self) -> List[Dict]:
        """Obtener todos los empleados de la BD"""
        empleados = self.db.query(Empleado).all()
        return [self._to_dict(e) for e in empleados]
    
    def get_by_id(self, id: int) -> Optional[Dict]:
        """Obtener un empleado por ID de la BD"""
        empleado = self.db.query(Empleado).filter(Empleado.id == id).first()
        return self._to_dict(empleado) if empleado else None
    
    def get_by_name(self, nombres: str) -> Optional[Dict]:
        """Obtener un empleado por nombre de la BD"""
        empleado = self.db.query(Empleado).filter(Empleado.nombres == nombres).first()
        return self._to_dict(empleado) if empleado else None
    
    def update(self, id: int, employee_data: Dict) -> Optional[Dict]:
        """Actualizar un empleado en la BD"""
        empleado = self.db.query(Empleado).filter(Empleado.id == id).first()
        if not empleado:
            return None
        
        for key, value in employee_data.items():
            setattr(empleado, key, value)
        
        self.db.commit()
        self.db.refresh(empleado)
        return self._to_dict(empleado)
    
    def delete(self, id: int) -> Optional[Dict]:
        """Eliminar un empleado de la BD"""
        empleado = self.db.query(Empleado).filter(Empleado.id == id).first()
        if empleado:
            resultado = self._to_dict(empleado)
            self.db.delete(empleado)
            self.db.commit()
            return resultado
        return None
    
    @staticmethod
    def _to_dict(empleado) -> Dict:
        """Convierte un modelo Empleado a diccionario"""
        if not empleado:
            return None
        return {
            "id": empleado.id,
            "nombres": empleado.nombres,
            "apellidos": empleado.apellidos,
            "estado": empleado.estado,
            "especialidad": empleado.especialidad,
        }
