from uuid import uuid4
from fastapi.testclient import TestClient
from main import app
from src.auth.infrastructure.auth import require_supabase_user


def override_require_supabase_user():
    return {"id": "test-user", "email": "test@demo.com"}


app.dependency_overrides[require_supabase_user] = override_require_supabase_user

client = TestClient(app)




def test_crear_servicio_particion_valida():
    nombre_unico = f"Servicio-{uuid4().hex[:8]}"
    payload = {
        "nombre": nombre_unico,
        "descripcion": "Servicio completo de revision y ajuste general",
    }

    response = client.post("/api/v1/servicios/", json=payload)

    assert response.status_code in [200, 201]
    data = response.json()
    assert data["nombre"] == nombre_unico


def test_crear_servicio_descripcion_corta():
    nombre_unico = f"Servicio-{uuid4().hex[:8]}"
    payload = {
        "nombre": nombre_unico,
        "descripcion": "Corto",
    }

    response = client.post("/api/v1/servicios/", json=payload)

    assert response.status_code == 400
