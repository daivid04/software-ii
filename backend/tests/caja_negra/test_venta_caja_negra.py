from uuid import uuid4
from datetime import datetime
from fastapi.testclient import TestClient
from main import app
from src.auth.infrastructure.auth import require_supabase_user


def override_require_supabase_user():
    return {"id": "test-user", "email": "test@demo.com"}


app.dependency_overrides[require_supabase_user] = override_require_supabase_user

client = TestClient(app)




def _crear_producto_base():
    nombre_unico = f"ProductoVenta-{uuid4().hex[:8]}"
    payload = {
        "nombre": nombre_unico,
        "descripcion": "Producto base para venta",
        "precio_compra": 50.0,
        "precio_venta": 90.0,
        "marca": "ACME",
        "categoria": "Ventas",
        "stock": 10,
        "stock_minimo": 1,
    }
    response = client.post("/api/v1/productos/", json=payload)
    assert response.status_code in [200, 201]
    return response.json()["id"]


def test_registrar_venta_particion_valida():
    producto_id = _crear_producto_base()

    payload = {
        "fecha": datetime.utcnow().isoformat(),
        "productos": [
            {
                "producto_id": producto_id,
                "cantidad": 2,
            }
        ],
    }

    response = client.post("/api/v1/ventas/", json=payload)

    assert response.status_code in [200, 201]
    data = response.json()
    assert data["id"] is not None


def test_registrar_venta_cantidad_invalida():
    producto_id = _crear_producto_base()

    payload = {
        "fecha": datetime.utcnow().isoformat(),
        "productos": [
            {
                "producto_id": producto_id,
                "cantidad": 0,
            }
        ],
    }

    response = client.post("/api/v1/ventas/", json=payload)

    assert response.status_code == 400
