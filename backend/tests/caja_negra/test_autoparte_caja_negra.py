import pytest
from uuid import uuid4
from fastapi.testclient import TestClient
from main import app
from src.auth.infrastructure.auth import require_supabase_user

def override_require_supabase_user():
    return {"id": "test-user", "email": "test@demo.com"}

app.dependency_overrides[require_supabase_user] = override_require_supabase_user

client = TestClient(app)

def test_registrar_autoparte_particion_valida():
    nombre_unico = f"Amortiguador-{uuid4().hex[:8]}"
    payload = {
        "nombre": nombre_unico,
        "descripcion": "Amortiguador para suspension delantera con buen rendimiento",
        "precio_compra": 80.0,
        "precio_venta": 120.5,
        "marca": "Monroe",
        "categoria": "Suspension",
        "stock": 15,
        "stock_minimo": 2,
        "modelo": "AMT-2024",
        "anio": "2020-2024"
    }
    
    response = client.post("/api/v1/autopartes/", json=payload)
    
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["nombre"] == nombre_unico
    assert data["stock"] == 15

def test_registrar_autoparte_limite_precio_negativo():
    payload_invalido = {
        "nombre": f"Bujia-{uuid4().hex[:8]}",
        "descripcion": "Bujia de encendido estandar para motor gasolina",
        "precio_compra": 50.0,
        "precio_venta": -5.0,  # Valor limite inferior rechazado
        "marca": "Bosch",
        "categoria": "Encendido",
        "stock": 10,
        "stock_minimo": 1,
        "modelo": "BJ-2020",
        "anio": "2018, 2020"
    }
    
    response = client.post("/api/v1/autopartes/", json=payload_invalido)
    assert response.status_code == 400

def test_actualizar_stock_limite_cero():
    payload_stock = {"stock": 0}
    response = client.put("/api/v1/autopartes/1/inventario", json=payload_stock)
    assert response.status_code in [200, 422, 404]
