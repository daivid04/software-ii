import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.hexagonal.adapters.primary.employee_api_adapter import router, get_employee_usecase
from backend.tests.hexagonal.mocks.mock_employee_usecase import MockEmployeeUseCase
from backend.core.auth import require_supabase_user

# Para propósitos de este test, crearemos una APP de prueba limpia que incluye el router usando los mocks.
app = FastAPI()
app.include_router(router, prefix="/employees")

# Simulamos la autenticación saltándola en las pruebas de Unit test del Adapter
def skip_auth():
    pass

app.dependency_overrides[require_supabase_user] = skip_auth

@pytest.fixture
def mock_usecase():
    return MockEmployeeUseCase()

@pytest.fixture
def client(mock_usecase):
    # Sobrescribimos el Use Case original inyectado por FastAPI con nuestro Mock.
    app.dependency_overrides[get_employee_usecase] = lambda: mock_usecase
    return TestClient(app)

def test_list_empleados(client: TestClient, mock_usecase: MockEmployeeUseCase):
    # DADO
    mock_usecase.set_mock_data([{"id": 1, "nombres": "Ana", "apellidos": "Lopez", "estado": "activo"}])
    
    # CUANDO
    response = client.get("/employees/")
    
    # ENTONCES
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["nombres"] == "Ana"

def test_get_empleado_not_found(client: TestClient, mock_usecase: MockEmployeeUseCase):
    # DADO
    mock_usecase.set_mock_data([])
    
    # CUANDO
    response = client.get("/employees/99")
    
    # ENTONCES
    assert response.status_code == 404
    assert response.json()["detail"] == "Empleado no encontrado"

def test_create_empleado(client: TestClient, mock_usecase: MockEmployeeUseCase):
    # DADO
    payload = {
        "nombres": "Juan",
        "apellidos": "Perez",
        "estado": "activo",
        "especialidad": "Mecanica"
    }
    
    # CUANDO
    response = client.post("/employees/", json=payload)
    
    # ENTONCES
    assert response.status_code == 200
    data = response.json()
    assert data["nombres"] == "Juan"
    assert data["id"] == 1

def test_create_empleado_handles_usecase_error(client: TestClient, mock_usecase: MockEmployeeUseCase):
    # DADO
    mock_usecase.should_raise_value_error = True
    payload = {
        "nombres": "Falla",
        "apellidos": "Falla",
        "estado": "activo",
    }
    
    # CUANDO
    response = client.post("/employees/", json=payload)
    
    # ENTONCES
    assert response.status_code == 400
    assert response.json()["detail"] == "Valor invalido forzado en prueba"
