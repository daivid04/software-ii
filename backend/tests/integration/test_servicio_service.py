import pytest
from unittest.mock import patch

import db.models 

from src.servicios.application.servicio_service import ServicioService
from src.servicios.infrastructure.servicio_schema import ServicioCreate
from tests.mocks.fake_repos import FakeServicioRepository

# --- PREPARACIÓN DEL ENTORNO ---
@pytest.fixture
def servicio_service():
    """Instancia el orquestador inyectando el repositorio en memoria"""
    service = ServicioService(db=None)
    service.repo = FakeServicioRepository()
    return service

# --- PRUEBAS DE INTEGRACIÓN ---

@patch('src.servicios.application.servicio_service.cache')
def test_registrar_nuevo_servicio_exito(mock_cache, servicio_service):
    """Verifica que el orquestador cree un servicio y limpie la caché"""
    
    # 1. Armamos la entrada
    data = ServicioCreate(
        nombre="Alineación 3D",
        descripcion="Alineación computarizada de dirección"
    )
    
    # 2. Ejecutamos
    resultado = servicio_service.registrar_nuevo_servicio(data)
    
    # 3. Verificamos guardado en memoria
    assert resultado.id == 1
    assert resultado.nombre == "Alineación 3D"
    assert len(servicio_service.repo.db_falsa) == 1
    
    # 4. Verificamos caché
    mock_cache.invalidate_pattern.assert_called_once_with('servicios')


@patch('src.servicios.application.servicio_service.cache')
def test_registrar_servicio_duplicado_falla(mock_cache, servicio_service):
    """Verifica que el servicio bloquee el registro si el nombre ya existe"""
    
    data = ServicioCreate(nombre="Balanceo", descripcion="Balanceo de llantas")
    
    # Guardamos el primero
    servicio_service.registrar_nuevo_servicio(data)
    
    # Intentamos duplicarlo
    with pytest.raises(ValueError) as excinfo:
        servicio_service.registrar_nuevo_servicio(data)
        
    assert "Ya existe un servicio con ese nombre" in str(excinfo.value)
    assert len(servicio_service.repo.db_falsa) == 1


@patch('src.servicios.application.servicio_service.cache')
def test_actualizar_informacion_servicio_exito(mock_cache, servicio_service):
    """Verifica el flujo de conversión a dominio y actualización"""
    
    # Precargamos un servicio
    data_inicial = ServicioCreate(nombre="Cambio de Aceite", descripcion="Mantenimiento básico")
    servicio_guardado = servicio_service.registrar_nuevo_servicio(data_inicial)
    
    # Creamos la data de actualización
    data_actualizada = ServicioCreate(
        nombre="Cambio de Aceite Premium", 
        descripcion="Incluye revisión de filtros y fluidos"
    )
    
    # Ejecutamos actualización
    resultado = servicio_service.actualizar_informacion_servicio(servicio_guardado.id, data_actualizada)
    
    # Verificamos
    assert resultado.nombre == "Cambio de Aceite Premium"
    assert "filtros y fluidos" in resultado.descripcion
    
    # Verificamos la limpieza de caché específica
    mock_cache.delete.assert_called_with(f'servicio_{servicio_guardado.id}')
    mock_cache.invalidate_pattern.assert_called_with('servicios')