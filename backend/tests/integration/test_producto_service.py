import pytest
from unittest.mock import patch

# --- SOLUCIÓN: Cargar todas las tablas para SQLAlchemy ---
import db.models 

from src.producto.application.producto_service import ProductoService
from src.producto.infrastructure.producto_schema import ProductoCreate
from tests.mocks.fake_repos import FakeProductoRepository

# --- PREPARACIÓN DEL ENTORNO ---
@pytest.fixture
def producto_service():
    """Instancia el orquestador inyectando el repositorio en memoria"""
    service = ProductoService(db=None)
    service.repo = FakeProductoRepository()
    return service

# --- PRUEBAS DE INTEGRACIÓN ---

@patch('src.producto.application.producto_service.cache')
def test_registrar_nuevo_producto_exito(mock_cache, producto_service):
    """Verifica que el servicio aplique reglas, guarde el producto e invalide caché"""
    
    # 1. Armamos el JSON de entrada con Pydantic
    data = ProductoCreate(
        nombre="Aceite Sintético 5W-30",
        descripcion="Aceite para motor a gasolina de alto rendimiento",
        precio_compra=30.0,
        precio_venta=55.0,
        marca="Castrol",
        categoria="Fluidos",
        stock=24,
        stock_minimo=6
    )
    
    # 2. Ejecutamos el caso de uso
    resultado = producto_service.registrar_nuevo_producto(data)
    
    # 3. Verificamos que se operó correctamente en memoria RAM
    assert resultado.id == 1
    assert resultado.nombre == "Aceite Sintético 5W-30"
    assert resultado.precio_venta == 55.0
    assert len(producto_service.repo.db_falsa) == 1
    
    # 4. Verificamos la limpieza de la memoria caché
    mock_cache.invalidate_pattern.assert_called_once_with('productos')


@patch('src.producto.application.producto_service.cache')
def test_registrar_producto_duplicado_falla(mock_cache, producto_service):
    """Verifica que el servicio bloquee el registro si el nombre ya existe"""
    
    data = ProductoCreate(
        nombre="Filtro de Aire", descripcion="Filtro estándar",
        precio_compra=10.0, precio_venta=20.0, marca="Bosch",
        categoria="Filtros", stock=10, stock_minimo=2
    )
    
    # Guardamos el primer registro
    producto_service.registrar_nuevo_producto(data)
    
    # Intentamos guardar exactamente el mismo producto
    with pytest.raises(ValueError) as excinfo:
        producto_service.registrar_nuevo_producto(data)
        
    assert "Ya existe un producto con ese nombre" in str(excinfo.value)
    # Verificamos que la tabla no haya crecido
    assert len(producto_service.repo.db_falsa) == 1


@patch('src.producto.application.producto_service.cache')
def test_actualizar_stock_y_precios_exito(mock_cache, producto_service):
    """Verifica el flujo de actualización de dominio sobre un producto existente"""
    
    # Precargamos un producto
    data_inicial = ProductoCreate(
        nombre="Bujía Iridium", descripcion="Bujía larga vida",
        precio_compra=8.0, precio_venta=15.0, marca="NGK",
        categoria="Encendido", stock=50, stock_minimo=10
    )
    producto_guardado = producto_service.registrar_nuevo_producto(data_inicial)
    
    # Creamos la data de actualización (Cambiamos stock y precios)
    data_actualizada = ProductoCreate(
        nombre="Bujía Iridium", descripcion="Bujía larga vida",
        precio_compra=10.0, precio_venta=18.0, marca="NGK",
        categoria="Encendido", stock=45, stock_minimo=10 # Descontamos 5
    )
    
    # Ejecutamos la actualización
    resultado = producto_service.actualizar_stock_y_precios(producto_guardado.id, data_actualizada)
    
    # Verificamos los cambios
    assert resultado.precio_venta == 18.0
    assert resultado.stock == 45
    # Verificamos que se borraron los cachés correctos
    mock_cache.delete.assert_called_with(f'producto_{producto_guardado.id}')