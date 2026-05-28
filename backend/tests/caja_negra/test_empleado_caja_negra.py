import pytest
from uuid import uuid4
from fastapi.testclient import TestClient
from main import app
from src.auth.infrastructure.auth import require_supabase_user

def override_require_supabase_user():
    return {"id": "test-user", "email": "test@demo.com"}

app.dependency_overrides[require_supabase_user] = override_require_supabase_user

client = TestClient(app)

def test_crear_empleado_particion_valida():
    nombres_unicos = f"Carlos-{uuid4().hex[:6]}"
    payload = {
        "nombres": nombres_unicos,
        "apellidos": "Santana",
        "estado": "activo",
        "especialidad": "Mecanica General"
    }
    
    response = client.post("/api/v1/empleados/", json=payload)
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["nombres"] == nombres_unicos
    assert data["estado"] == "activo"

def test_crear_empleado_valor_limite_nombre_corto():
    payload = {
        "nombres": "A",
        "apellidos": "Ruiz",
        "estado": "activo",
        "especialidad": "Electricidad"
    }
    
    response = client.post("/api/v1/empleados/", json=payload)
    
    assert response.status_code == 400

def test_crear_empleado_particion_invalida_estado():
    payload = {
        "nombres": "Ana",
        "apellidos": "García",
        "estado": "suspendido_temporalmente",
        "especialidad": "Pintura"
    }
    
    response = client.post("/api/v1/empleados/", json=payload)
    assert response.status_code == 400
