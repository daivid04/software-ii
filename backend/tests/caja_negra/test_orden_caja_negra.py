from uuid import uuid4
from datetime import date
from fastapi.testclient import TestClient
from main import app
from src.auth.infrastructure.auth import require_supabase_user


def override_require_supabase_user():
    return {"id": "test-user", "email": "test@demo.com"}


app.dependency_overrides[require_supabase_user] = override_require_supabase_user

client = TestClient(app)




def _crear_servicio_base():
    nombre_unico = f"ServicioOrden-{uuid4().hex[:8]}"
    payload = {
        "nombre": nombre_unico,
        "descripcion": "Servicio base para orden de trabajo",
    }
    response = client.post("/api/v1/servicios/", json=payload)
    assert response.status_code in [200, 201]
    return response.json()["id"]


def _crear_empleado_base():
    nombres_unicos = f"Empleado-{uuid4().hex[:6]}"
    payload = {
        "nombres": nombres_unicos,
        "apellidos": "Gomez",
        "estado": "activo",
        "especialidad": "Mecanica",
    }
    response = client.post("/api/v1/empleados/", json=payload)
    assert response.status_code in [200, 201]
    return response.json()["id"]


def test_crear_orden_particion_valida():
    servicio_id = _crear_servicio_base()
    empleado_id = _crear_empleado_base()

    payload = {
        "garantia": 6,
        "estadoPago": "pendiente",
        "precio": 120,
        "fecha": date.today().isoformat(),
        "servicios": [
            {
                "servicio_id": servicio_id,
                "precio_servicio": 120,
            }
        ],
        "empleados": [
            {
                "empleado_id": empleado_id,
            }
        ],
    }

    response = client.post("/api/v1/ordenes/", json=payload)

    assert response.status_code in [200, 201]
    data = response.json()
    assert data["estadoPago"] == "pendiente"


def test_crear_orden_estado_pago_invalido():
    payload = {
        "garantia": 6,
        "estadoPago": "pagando",
        "precio": 120,
        "fecha": date.today().isoformat(),
        "servicios": [],
        "empleados": [],
    }

    response = client.post("/api/v1/ordenes/", json=payload)

    assert response.status_code == 400
