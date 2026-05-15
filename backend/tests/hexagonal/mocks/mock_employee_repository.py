from typing import List, Optional, Dict
from backend.hexagonal.ports.employee_driven_port import EmployeeRepository

class MockEmployeeRepository(EmployeeRepository):
    """
    Mock en memoria del repositorio de empleados para pruebas unitarias.
    Actúa como un 'Stub' para simular la base de datos externa interactuando visualmente 
    a través del puerto de salida (driven port).
    """
    def __init__(self):
        self._employees = {}
        self._current_id = 1

    def reset_mock(self):
        """Reinicia el estado del mock para evitar cruce de datos entre pruebas."""
        self._employees.clear()
        self._current_id = 1

    def create(self, employee_data: Dict) -> Dict:
        emp_id = self._current_id
        
        # Clonamos para no modificar la referencia externa
        new_employee = employee_data.copy()
        new_employee["id"] = emp_id
        
        self._employees[emp_id] = new_employee
        self._current_id += 1
        return new_employee

    def get_all(self) -> List[Dict]:
        return list(self._employees.values())

    def get_by_id(self, id: int) -> Optional[Dict]:
        return self._employees.get(id)

    def get_by_name(self, nombres: str) -> Optional[Dict]:
        for emp in self._employees.values():
            if emp.get("nombres") == nombres:
                return emp
        return None

    def update(self, id: int, employee_data: Dict) -> Optional[Dict]:
        if id in self._employees:
            self._employees[id].update(employee_data)
            self._employees[id]["id"] = id 
            return self._employees[id]
        return None

    def delete(self, id: int) -> Optional[Dict]:
        if id in self._employees:
            return self._employees.pop(id)
        return None
