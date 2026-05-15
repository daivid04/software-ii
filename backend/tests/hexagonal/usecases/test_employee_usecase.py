import pytest
from typing import Dict
from backend.hexagonal.usecases.employee_usecase import EmployeeUseCase
from backend.tests.hexagonal.mocks.mock_employee_repository import MockEmployeeRepository

@pytest.fixture
def mock_emp_repo() -> MockEmployeeRepository:
    """Provee una instancia fresca del puerto secundario mockeado para cada test"""
    return MockEmployeeRepository()

@pytest.fixture
def employee_usecase(mock_emp_repo: MockEmployeeRepository) -> EmployeeUseCase:
    """Provee el caso de uso instanciado con el mock del repositorio"""
    return EmployeeUseCase(repository=mock_emp_repo)

def test_create_employee_success(employee_usecase: EmployeeUseCase, mock_emp_repo: MockEmployeeRepository):
    # DADO (Arrange)
    employee_data = {"nombres": "Juan", "rol": "Mecánico"}
    
    # CUANDO (Act)
    result = employee_usecase.create_employee(employee_data)
    
    # ENTONCES (Assert)
    assert result["id"] == 1
    assert result["nombres"] == "Juan"

def test_create_employee_duplicate_name_raises_value_error(employee_usecase: EmployeeUseCase):
    # DADO (Arrange)
    employee_data = {"nombres": "Maria", "rol": "Administrador"}
    employee_usecase.create_employee(employee_data)
    
    # CUANDO / ENTONCES (Act/Assert)
    with pytest.raises(ValueError, match="Ya existe un empleado con ese nombre"):
        employee_usecase.create_employee(employee_data)

def test_list_employees(employee_usecase: EmployeeUseCase):
    # DADO (Arrange)
    employee_usecase.create_employee({"nombres": "Pedro"})
    employee_usecase.create_employee({"nombres": "Ana"})
    
    # CUANDO (Act)
    result = employee_usecase.list_employees()
    
    # ENTONCES (Assert)
    assert len(result) == 2
    assert result[0]["nombres"] == "Pedro"
    assert result[1]["nombres"] == "Ana"

def test_update_employee(employee_usecase: EmployeeUseCase):
    # DADO (Arrange)
    created = employee_usecase.create_employee({"nombres": "Carlos", "telefono": "123"})
    
    # CUANDO (Act)
    updated = employee_usecase.update_employee(created["id"], {"telefono": "999"})
    
    # ENTONCES (Assert)
    assert updated is not None
    assert updated["telefono"] == "999"
    assert updated["nombres"] == "Carlos"

def test_delete_employee(employee_usecase: EmployeeUseCase, mock_emp_repo: MockEmployeeRepository):
    # DADO (Arrange)
    created = employee_usecase.create_employee({"nombres": "Luis"})
    assert mock_emp_repo.get_by_id(created["id"]) is not None
    
    # CUANDO (Act)
    deleted = employee_usecase.delete_employee(created["id"])
    
    # ENTONCES (Assert)
    assert deleted["nombres"] == "Luis"
    assert mock_emp_repo.get_by_id(created["id"]) is None
