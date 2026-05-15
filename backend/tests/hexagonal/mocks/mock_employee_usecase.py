from typing import Dict, List, Optional
from backend.hexagonal.usecases.employee_usecase import EmployeeUseCase
from backend.hexagonal.ports.employee_driving_ports import (
    CreateEmployeePort,
    ListEmployeesPort,
    GetEmployeePort,
    UpdateEmployeePort,
    DeleteEmployeePort,
)

class MockEmployeeUseCase(
    CreateEmployeePort,
    ListEmployeesPort,
    GetEmployeePort,
    UpdateEmployeePort,
    DeleteEmployeePort
):
    """
    Mock del UseCase de Empleados.
    Se usa para aislar la capa del adaptador primario (FastAPI) de la lógica de negocio
    y de la base de datos real durante pruebas de controladores.
    """
    def __init__(self):
        self.mock_employees: List[Dict] = []
        self.should_raise_value_error: bool = False
    
    def set_mock_data(self, employees: List[Dict]):
        self.mock_employees = employees
        
    def create_employee(self, employee_data: Dict) -> Dict:
        if self.should_raise_value_error:
            raise ValueError("Valor invalido forzado en prueba")
        
        new_emp = employee_data.copy()
        new_emp["id"] = len(self.mock_employees) + 1
        self.mock_employees.append(new_emp)
        return new_emp

    def list_employees(self) -> List[Dict]:
        return self.mock_employees

    def get_employee(self, id: int) -> Optional[Dict]:
        for emp in self.mock_employees:
            if emp.get("id") == id:
                return emp
        return None

    def update_employee(self, id: int, employee_data: Dict) -> Optional[Dict]:
        for emp in self.mock_employees:
            if emp.get("id") == id:
                emp.update(employee_data)
                return emp
        return None

    def delete_employee(self, id: int) -> Optional[Dict]:
        for i, emp in enumerate(self.mock_employees):
            if emp.get("id") == id:
                return self.mock_employees.pop(i)
        return None
