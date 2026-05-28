from uuid import uuid4
from fastapi.testclient import TestClient
from main import app
from src.auth.infrastructure.auth import require_supabase_user


def override_require_supabase_user():
    return {"id": "test-user", "email": "test@demo.com"}


app.dependency_overrides[require_supabase_user] = override_require_supabase_user

client = TestClient(app)




def test_crear_producto_particion_valida():
    nombre_unico = f"Filtro-{uuid4().hex[:8]}"
    payload = {
        "nombre": nombre_unico,
        "descripcion": "Filtro de aceite para motor, uso diario",
        "precio_compra": 100.0,
        "precio_venta": 150.0,
        "marca": "Bosch",
        "categoria": "Motor",
        "stock": 20,
        "stock_minimo": 2,
    }

    response = client.post("/api/v1/productos/", json=payload)

    assert response.status_code in [200, 201]
    data = response.json()
    assert data["nombre"] == nombre_unico
    assert data["stock"] == 20


def test_crear_producto_precio_venta_invalido():
    nombre_unico = f"Producto-{uuid4().hex[:8]}"
    payload = {
        "nombre": nombre_unico,
        "descripcion": "Producto de prueba con precio invalido",
        "precio_compra": 200.0,
        "precio_venta": 150.0,
        "marca": "ACME",
        "categoria": "Pruebas",
        "stock": 5,
        "stock_minimo": 1,
    }

    response = client.post("/api/v1/productos/", json=payload)

    assert response.status_code == 400
