import pytest
from typing import Dict
from backend.hexagonal.usecases.employee_usecase import EmployeeUseCase
from backend.tests.hexagonal.mocks.mock_employee_repository import MockEmployeeRepository

class TestEmployeeUseCase:
    """Agrupación de pruebas con inicialización equivalente a beforeEach"""

    def setup_method(self):
        """
        Actúa exactamente como beforeEach() en otros lenguajes.
        Se ejecuta antes de CADA prueba individual para evitar contaminación de estado.
        """
        self.mock_repo = MockEmployeeRepository()
        self.usecase = EmployeeUseCase(repository=self.mock_repo)

    def test_create_employee_success(self):
        # DADO
        employee_data = {"nombres": "Juan", "rol": "Mecánico"}
        
        # CUANDO
        result = self.usecase.create_employee(employee_data)
        
        # ENTONCES
        assert result["id"] == 1
        assert result["nombres"] == "Juan"

    def test_create_employee_duplicate_name_raises_value_error(self):
        # DADO
        employee_data = {"nombres": "Maria", "rol": "Administrador"}
        self.usecase.create_employee(employee_data)
        
        # CUANDO / ENTONCES
        with pytest.raises(ValueError, match="Ya existe un empleado con ese nombre"):
            self.usecase.create_employee(employee_data)

    def test_list_employees(self):
        # DADO
        self.usecase.create_employee({"nombres": "Pedro"})
        self.usecase.create_employee({"nombres": "Ana"})
        
        # CUANDO
        result = self.usecase.list_employees()
        
        # ENTONCES
        assert len(result) == 2
        assert result[0]["nombres"] == "Pedro"
        assert result[1]["nombres"] == "Ana"

    def test_update_employee(self):
        # DADO
        created = self.usecase.create_employee({"nombres": "Carlos", "telefono": "123"})
        
        # CUANDO
        updated = self.usecase.update_employee(created["id"], {"telefono": "999"})
        
        # ENTONCES
        assert updated is not None
        assert updated["telefono"] == "999"

    def test_delete_employee(self):
        # DADO
        created = self.usecase.create_employee({"nombres": "Luis"})
        assert self.mock_repo.get_by_id(created["id"]) is not None
        
        # CUANDO
        deleted = self.usecase.delete_employee(created["id"])
        
        # ENTONCES
        assert deleted["nombres"] == "Luis"
        assert self.mock_repo.get_by_id(created["id"]) is None
