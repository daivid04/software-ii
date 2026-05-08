"""
Caso de Uso (Use Case) - Lógica de negocio de Empleado
Implementa los Puertos Primarios (Driving Ports)
Depende de los Puertos Secundarios (Driven Ports)
"""
from typing import Dict, List, Optional
from hexagonal.ports.employee_driven_port import EmployeeRepository
from hexagonal.ports.employee_driving_ports import (
    CreateEmployeePort,
    ListEmployeesPort,
    GetEmployeePort,
    UpdateEmployeePort,
    DeleteEmployeePort,
)

class EmployeeUseCase(
    CreateEmployeePort,
    ListEmployeesPort,
    GetEmployeePort,
    UpdateEmployeePort,
    DeleteEmployeePort,
):
    """
    Caso de uso para Empleado
    Implementa todos los puertos primarios
    Depende del repositorio (puerto secundario)
    """
    
    def __init__(self, repository: EmployeeRepository):
        self.repository = repository
    
    def create_employee(self, employee_data: Dict) -> Dict:
        """Crear un nuevo empleado con validaciones"""
        # Validación: no permitir empleados duplicados por nombre
        if self.repository.get_by_name(employee_data.get("nombres")):
            raise ValueError("Ya existe un empleado con ese nombre")
        
        return self.repository.create(employee_data)
    
    def list_employees(self) -> List[Dict]:
        """Obtener lista de todos los empleados"""
        return self.repository.get_all()
    
    def get_employee(self, id: int) -> Optional[Dict]:
        """Obtener un empleado por su ID"""
        return self.repository.get_by_id(id)
    
    def update_employee(self, id: int, employee_data: Dict) -> Optional[Dict]:
        """Actualizar un empleado existente"""
        return self.repository.update(id, employee_data)
    
    def delete_employee(self, id: int) -> Optional[Dict]:
        """Eliminar un empleado"""
        return self.repository.delete(id)
