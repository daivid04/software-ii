import pytest
from src.shared.domain.value_objects import EstadoEmpleadoVO
from src.empleados.domain.empleado_domain import EmpleadoDomain

# --- PRUEBAS DE VALUE OBJECTS ---

def test_estado_empleado_vo_valido():
    """Prueba que un estado válido se asigne correctamente"""
    # Tu Value Object acepta 'activo' (en minúscula según su propio mensaje de error)
    estado = EstadoEmpleadoVO("activo")
    assert estado.valor == "activo"

def test_estado_empleado_vo_invalido():
    """Prueba que un estado inválido levante un error ValueError"""
    with pytest.raises(ValueError) as excinfo:
        EstadoEmpleadoVO("despedido")
    
    # Verificamos que el mensaje contenga el texto real que emite tu código
    assert "Estado de empleado no válido" in str(excinfo.value)

# --- PRUEBAS DEL AGREGADO (EMPLEADO DOMAIN) ---

def test_empleado_domain_cambiar_estado():
    """Prueba que el empleado actualice su estado a través de la regla de negocio"""
    # 1. Instanciamos un empleado nuevo (por defecto está activo)
    empleado = EmpleadoDomain(nombres="Juan", apellidos="Pérez")
    assert empleado.estado == "activo"
    
    # 2. Cambiamos el estado usando el método del dominio
    empleado.cambiar_estado("inactivo")
    
    # 3. Verificamos que el estado interno cambió
    assert empleado.estado == "inactivo"