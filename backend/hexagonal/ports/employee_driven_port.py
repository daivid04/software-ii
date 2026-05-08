"""
Puerto Secundario (Driven Port)
Define las operaciones que la aplicación necesita del mundo externo (base de datos)
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict

class EmployeeRepository(ABC):
    """Interface - Puerto Secundario para persistencia de Empleados"""
    
    @abstractmethod
    def create(self, employee_data: Dict) -> Dict:
        """Crear un empleado"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Dict]:
        """Obtener todos los empleados"""
        pass
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Dict]:
        """Obtener empleado por ID"""
        pass
    
    @abstractmethod
    def get_by_name(self, nombres: str) -> Optional[Dict]:
        """Obtener empleado por nombre"""
        pass
    
    @abstractmethod
    def update(self, id: int, employee_data: Dict) -> Optional[Dict]:
        """Actualizar un empleado"""
        pass
    
    @abstractmethod
    def delete(self, id: int) -> Optional[Dict]:
        """Eliminar un empleado"""
        pass
