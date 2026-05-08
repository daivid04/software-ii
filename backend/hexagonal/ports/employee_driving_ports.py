"""
Puertos Primarios (Driving Ports)
Define los casos de uso que expone la aplicación al mundo externo
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict

class CreateEmployeePort(ABC):
    """Puerto Primario - Caso de uso: Crear empleado"""
    
    @abstractmethod
    def create_employee(self, employee_data: Dict) -> Dict:
        pass

class ListEmployeesPort(ABC):
    """Puerto Primario - Caso de uso: Listar empleados"""
    
    @abstractmethod
    def list_employees(self) -> List[Dict]:
        pass

class GetEmployeePort(ABC):
    """Puerto Primario - Caso de uso: Obtener empleado por ID"""
    
    @abstractmethod
    def get_employee(self, id: int) -> Optional[Dict]:
        pass

class UpdateEmployeePort(ABC):
    """Puerto Primario - Caso de uso: Actualizar empleado"""
    
    @abstractmethod
    def update_employee(self, id: int, employee_data: Dict) -> Optional[Dict]:
        pass

class DeleteEmployeePort(ABC):
    """Puerto Primario - Caso de uso: Eliminar empleado"""
    
    @abstractmethod
    def delete_employee(self, id: int) -> Optional[Dict]:
        pass
