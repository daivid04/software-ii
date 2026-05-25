import pytest
from datetime import datetime, timezone
from unittest.mock import patch
from fastapi import HTTPException

# --- SOLUCIÓN: Cargar todas las tablas para SQLAlchemy ---
import db.models 

from src.ventas.application.venta_service import VentaService
from src.ventas.infrastructure.venta_schema import VentaCreate, VentaProductoBase
from src.producto.infrastructure.producto import Producto
from tests.mocks.fake_repos import FakeVentaRepository, FakeProductoRepository

# --- PREPARACIÓN DEL ENTORNO ---
@pytest.fixture
def venta_service():
    """Instancia el orquestador inyectando repositorios falsos para Ventas y Productos"""
    service = VentaService(db=None)
    service.repo = FakeVentaRepository()
    service.producto_repo = FakeProductoRepository()
    
    # Precargamos un producto ORM real en la BD falsa para que el servicio pueda 
    # ejecutar el .to_domain() y el .from_domain() sin explotar
    producto_dummy = Producto(
        id=10, nombre="Llantas Aro 15", descripcion="Llantas de aleación", 
        marca="Michelin", categoria="Ruedas", precio_compra=100.0, 
        precio_venta=150.0, stock=4, stock_minimo=2, tipo="producto"
    )
    service.producto_repo.db_falsa.append(producto_dummy)
    
    return service

# --- PRUEBAS DE INTEGRACIÓN ---

@patch('src.ventas.application.venta_service.cache')
def test_registrar_venta_flujo_completo_exito(mock_cache, venta_service):
    """Verifica el Happy Path: Orquestación, descuento de stock y guardado"""
    
    # 1. Armamos la entrada (Compramos 3 llantas, quedan 1 en stock)
    data = VentaCreate(
        fecha=datetime.now(timezone.utc),
        productos=[VentaProductoBase(producto_id=10, cantidad=3)]
    )
    
    # 2. Ejecutamos el caso de uso
    resultado = venta_service.registrar_nueva_venta(data)
    
    # 3. Verificamos que la venta se guardó correctamente
    assert resultado.id == 1
    assert len(resultado.productos) == 1
    assert len(venta_service.repo.db_falsa) == 1
    
    # 4. Verificamos que el stock del producto disminuyó en el otro repositorio
    producto_actualizado = venta_service.producto_repo.consultar_producto(10)
    assert producto_actualizado.stock == 1 # Tenía 4, compró 3
    
    # 5. Verificación de caché
    mock_cache.invalidate_pattern.assert_any_call('productos')
    mock_cache.invalidate_pattern.assert_any_call('autopartes')


@patch('src.ventas.application.venta_service.cache')
def test_registrar_venta_falla_por_quiebre_de_stock(mock_cache, venta_service):
    """Verifica que el servicio aborte y lance Error HTTP 400 si el dominio rechaza por stock"""
    
    # Intentamos comprar 5 llantas (solo hay 4 en stock)
    data = VentaCreate(
        fecha=datetime.now(timezone.utc),
        productos=[VentaProductoBase(producto_id=10, cantidad=5)]
    )
    
    # El servicio debe atrapar el ValueError del Dominio y transformarlo en HTTPException
    with pytest.raises(HTTPException) as excinfo:
        venta_service.registrar_nueva_venta(data)
        
    assert excinfo.value.status_code == 400
    assert "insuficiente" in excinfo.value.detail.lower()
    
    # Fundamental: Verificamos que la tabla de ventas sigue vacía (Transacción abortada)
    assert len(venta_service.repo.db_falsa) == 0
    
    # Fundamental 2: Verificamos que el stock del producto NO bajó
    producto_intacto = venta_service.producto_repo.consultar_producto(10)
    assert producto_intacto.stock == 4