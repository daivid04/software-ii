import pytest
from datetime import date
from unittest.mock import patch
from fastapi import HTTPException

import db.models

from src.ordenes.application.orden_service import OrdenService
from src.ordenes.infrastructure.orden_schema import OrdenCreate, OrdenServicioBase, OrdenEmpleadoBase
from tests.mocks.fake_repos import FakeOrdenRepository, FakeServicioRepository, FakeEmpleadoRepository

# Clases falsas miniatura para simular la respuesta de PostgreSQL
class MockEmpleadoORM:
    def __init__(self, id, estado, nombres):
        self.id = id
        self.estado = estado
        self.nombres = nombres

class MockServicioORM:
    def __init__(self, id):
        self.id = id

# --- PREPARACIÓN DEL ENTORNO ---
@pytest.fixture
def orden_service():
    """Instancia el orquestador y le inyecta las tres bases de datos falsas"""
    service = OrdenService(db=None)
    service.repo = FakeOrdenRepository()
    service.servicio_repo = FakeServicioRepository()
    service.empleado_repo = FakeEmpleadoRepository()
    
    # "Llenamos" las tablas falsas con datos para que la Orden pueda consultarlos
    service.empleado_repo.db_falsa.append(MockEmpleadoORM(id=5, estado="activo", nombres="Juan Pérez"))
    service.empleado_repo.db_falsa.append(MockEmpleadoORM(id=9, estado="inactivo", nombres="Luis Gómez"))
    service.servicio_repo.db_falsa.append(MockServicioORM(id=10))
    
    return service

# --- PRUEBAS DE INTEGRACIÓN ---

@patch('src.ordenes.application.orden_service.cache')
def test_registrar_orden_exito(mock_cache, orden_service):
    """Verifica el Happy Path: Orquestación, guardado y limpieza de caché"""
    # 1. Armamos el JSON de entrada con la estructura estricta de Pydantic
    data = OrdenCreate(
        garantia=6,
        estadoPago="pendiente",
        precio=1500,
        fecha=date.today(),
        servicios=[OrdenServicioBase(servicio_id=10, precio_servicio=500)],
        empleados=[OrdenEmpleadoBase(empleado_id=5)] # Empleado activo
    )
    
    # 2. Ejecutamos el caso de uso
    resultado = orden_service.registrar_nueva_orden(data)
    
    # 3. Verificamos los resultados
    assert resultado.id == 1
    assert resultado.garantia == 6
    assert len(resultado.empleados) == 1
    assert len(orden_service.repo.db_falsa) == 1
    mock_cache.invalidate_pattern.assert_called_once_with('ordenes')


@patch('src.ordenes.application.orden_service.cache')
def test_registrar_orden_falla_por_empleado_inactivo(mock_cache, orden_service):
    """Verifica que el servicio aborte y lance un Error HTTP 400 por regla de negocio"""
    
    data = OrdenCreate(
        garantia=6, estadoPago="pendiente", precio=1500, fecha=date.today(),
        servicios=[OrdenServicioBase(servicio_id=10, precio_servicio=500)],
        empleados=[OrdenEmpleadoBase(empleado_id=9)] # <--- Empleado inactivo
    )
    
    # Atrapamos el HTTPException que tu código lanza
    with pytest.raises(HTTPException) as excinfo:
        orden_service.registrar_nueva_orden(data)
        
    # Verificamos que sea un error 400 Bad Request
    assert excinfo.value.status_code == 400
    # Verificamos que el mensaje del dominio haya viajado hasta el error HTTP
    assert "no está activo" in excinfo.value.detail.lower()
    
    # Fundamental: Verificamos que la tabla de órdenes sigue vacía (se bloqueó el guardado)
    assert len(orden_service.repo.db_falsa) == 0