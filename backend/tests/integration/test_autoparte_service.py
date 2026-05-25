import pytest
from unittest.mock import patch

# --- SOLUCIÓN: Cargar todas las tablas para SQLAlchemy ---
import db.models 

from src.autopartes.application.autoparte_service import AutoparteService
from src.autopartes.infrastructure.autoparte_schema import AutoparteCreate
from tests.mocks.fake_repos import FakeAutoparteRepository

# --- PREPARACIÓN DEL ENTORNO ---
@pytest.fixture
def autoparte_service():
    """Instancia el orquestador inyectando el repositorio en memoria"""
    service = AutoparteService(db=None)
    service.repo = FakeAutoparteRepository()
    return service

# --- PRUEBAS DE INTEGRACIÓN ---

@patch('src.autopartes.application.autoparte_service.cache')
def test_registrar_nueva_autoparte_exito(mock_cache, autoparte_service):
    """Verifica que el orquestador cree una autoparte con su compatibilidad de vehículo"""
    
    # 1. Armamos el JSON de entrada con Pydantic
    data = AutoparteCreate(
        nombre="Filtro de Aceite Hilux",
        descripcion="Filtro original para Toyota",
        precio_compra=25.0,
        precio_venta=45.0,
        marca="Toyota",
        categoria="Filtros",
        stock=15,
        stock_minimo=3,
        modelo="Toyota Hilux",
        anio="2018-2023"
    )
    
    # 2. Ejecutamos el caso de uso
    resultado = autoparte_service.registrar_nueva_autoparte(data)
    
    # 3. Verificamos que se operó correctamente en memoria RAM
    assert resultado.id == 1
    assert resultado.nombre == "Filtro de Aceite Hilux"
    assert getattr(resultado, 'modelo', None) == "Toyota Hilux"
    assert len(autoparte_service.repo.db_falsa) == 1
    
    # 4. Verificamos la limpieza de la memoria caché
    mock_cache.invalidate_pattern.assert_called_once_with('autopartes')


@patch('src.autopartes.application.autoparte_service.cache')
def test_registrar_autoparte_duplicada_falla(mock_cache, autoparte_service):
    """Verifica que el servicio bloquee el registro si la autoparte ya existe"""
    
    data = AutoparteCreate(
        nombre="Bomba de Agua", descripcion="Bomba genérica",
        precio_compra=50.0, precio_venta=90.0, marca="GMB",
        categoria="Motor", stock=5, stock_minimo=1,
        modelo="Universal", anio="2010-2020"
    )
    
    # Guardamos el primer registro
    autoparte_service.registrar_nueva_autoparte(data)
    
    # Intentamos guardar exactamente el mismo
    with pytest.raises(ValueError) as excinfo:
        autoparte_service.registrar_nueva_autoparte(data)
        
    assert "Ya existe una autoparte con ese nombre" in str(excinfo.value)
    assert len(autoparte_service.repo.db_falsa) == 1


@patch('src.autopartes.application.autoparte_service.cache')
def test_actualizar_informacion_autoparte_exito(mock_cache, autoparte_service):
    """Verifica que la lógica de conversión a dominio y actualización funcione"""
    
    # Precargamos una autoparte
    data_inicial = AutoparteCreate(
        nombre="Pastillas de Freno", descripcion="Cerámicas",
        precio_compra=40.0, precio_venta=70.0, marca="Bosch",
        categoria="Frenos", stock=20, stock_minimo=4,
        modelo="Nissan Sentra", anio="2015-2019"
    )
    autoparte_guardada = autoparte_service.registrar_nueva_autoparte(data_inicial)
    
    # Creamos la data de actualización (Cambiamos el modelo y el stock)
    data_actualizada = AutoparteCreate(
        nombre="Pastillas de Freno", descripcion="Cerámicas",
        precio_compra=40.0, precio_venta=70.0, marca="Bosch",
        categoria="Frenos", stock=15, stock_minimo=4, # Descontamos 5
        modelo="Nissan Sentra / Versa", anio="2015-2022" # Ampliamos compatibilidad
    )
    
    # Ejecutamos la actualización
    resultado = autoparte_service.actualizar_informacion_autoparte(autoparte_guardada.id, data_actualizada)
    
    # Verificamos los cambios
    assert getattr(resultado, 'stock', None) == 15
    assert getattr(resultado, 'modelo', None) == "Nissan Sentra / Versa"
    
    # Verificamos invalidación de caché
    mock_cache.delete.assert_called_with(f'producto_{autoparte_guardada.id}')
    mock_cache.invalidate_pattern.assert_called_with('productos')