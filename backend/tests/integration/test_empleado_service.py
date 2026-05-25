import pytest
from unittest.mock import patch
from src.empleados.application.empleado_service import EmpleadoService
from src.empleados.infrastructure.empleado_schema import EmpleadoCreate
from tests.mocks.fake_repos import FakeEmpleadoRepository
import db.models

# --- PREPARACIÓN DEL ENTORNO AISLADO ---
@pytest.fixture
def empleado_service():
    """Crea una instancia del servicio inyectándole la base de datos falsa"""
    service = EmpleadoService(db=None) # Aislamos de la BD real
    service.repo = FakeEmpleadoRepository() # Inyectamos el Mock
    return service

# --- PRUEBAS DE INTEGRACIÓN (FASE 4) ---

@patch('src.empleados.application.empleado_service.cache')
def test_registrar_nuevo_empleado_exito(mock_cache, empleado_service):
    """Prueba que el orquestador cree un empleado y limpie la caché"""
    
    # 1. Datos de entrada (Simulando el JSON de FastAPI)
    data = EmpleadoCreate(
        nombres="Roberto",
        apellidos="Gómez",
        estado="activo",
        especialidad="Frenos y Suspensión"
    )
    
    # 2. Ejecutamos el caso de uso
    resultado = empleado_service.registrar_nuevo_empleado(data)
    
    # 3. Verificamos que se guardó correctamente en el repo falso
    assert resultado.id == 1
    assert resultado.nombres == "Roberto"
    assert len(empleado_service.repo.db_falsa) == 1
    
    # 4. Verificamos que el orquestador mandó a limpiar la memoria caché
    mock_cache.invalidate_pattern.assert_called_once_with('empleados')

@patch('src.empleados.application.empleado_service.cache')
def test_registrar_empleado_duplicado_falla(mock_cache, empleado_service):
    """Prueba que el orquestador detecte nombres duplicados antes de tocar el dominio"""
    
    data = EmpleadoCreate(
        nombres="Roberto", apellidos="Gómez", estado="activo", especialidad="Frenos"
    )
    
    # Registramos el primero con éxito
    empleado_service.registrar_nuevo_empleado(data)
    
    # Intentamos registrar exactamente el mismo
    with pytest.raises(ValueError) as excinfo:
        empleado_service.registrar_nuevo_empleado(data)
        
    assert "Ya existe un empleado registrado con esos nombres" in str(excinfo.value)

@patch('src.empleados.application.empleado_service.cache')
def test_dar_de_baja_empleado_exito(mock_cache, empleado_service):
    """Prueba el flujo completo de eliminación"""
    
    # Precargamos un empleado en la BD falsa
    data = EmpleadoCreate(nombres="Luis", apellidos="Pérez", estado="activo", especialidad="Motor")
    empleado_guardado = empleado_service.registrar_nuevo_empleado(data)
    
    # Ejecutamos el borrado
    resultado = empleado_service.dar_de_baja_empleado(empleado_guardado.id)
    
    # Verificamos que el repo falso quedó vacío
    assert resultado is not None
    assert len(empleado_service.repo.db_falsa) == 0
    # Verificamos que se invalidó el caché tras borrar
    mock_cache.delete.assert_called_with(f'empleado_{empleado_guardado.id}')