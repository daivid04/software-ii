import pytest
from datetime import date
from src.ordenes.domain.orden_domain import OrdenDomain

# ==========================================
# PRUEBAS DEL AGREGADO RAÍZ: ORDEN DOMAIN
# ==========================================

def test_orden_domain_inicializacion_correcta():
    """Prueba que los datos básicos se asignen y validen correctamente a través de los VOs internos"""
    orden = OrdenDomain()
    fecha_actual = date.today()
    
    # Llamamos al método del dominio
    orden.inicializar_datos_basicos(
        garantia=6, 
        estadoPago="pendiente", 
        precio=1500, 
        fecha=fecha_actual
    )
    
    # Verificamos que el estado interno mutó correctamente
    assert orden.garantia == 6
    assert orden.estadoPago == "pendiente"
    assert orden.precio == 1500
    assert orden.fecha == fecha_actual

def test_orden_domain_agregar_servicio():
    """Prueba que la orden orqueste correctamente la adición de servicios"""
    orden = OrdenDomain()
    
    orden.agregar_servicio(servicio_id=1, precio_servicio=500)
    orden.agregar_servicio(servicio_id=2, precio_servicio=1000)
    
    assert len(orden.servicios) == 2
    assert orden.servicios[0]["servicio_id"] == 1
    assert orden.servicios[1]["precio_servicio"] == 1000

def test_orden_domain_asignar_empleado_exito():
    """Prueba que se pueda asignar un empleado si está activo"""
    orden = OrdenDomain()
    
    # El dominio recibe los datos puros (sin ORMs) y valida la regla
    orden.asignar_empleado(empleado_id=5, estado_empleado="activo", nombre_empleado="Carlos")
    
    assert len(orden.empleados) == 1
    assert orden.empleados[0]["empleado_id"] == 5

def test_orden_domain_asignar_empleado_inactivo_falla():
    """Prueba que el Dominio BLINDE la orden y rechace empleados inactivos (Invariante del negocio)"""
    orden = OrdenDomain()
    
    # Intentamos asignar a un empleado que está de vacaciones o inactivo
    with pytest.raises(ValueError) as excinfo:
        orden.asignar_empleado(empleado_id=8, estado_empleado="vacaciones", nombre_empleado="Luis")
    
    # Verificamos que el dominio lo rechazó con el mensaje correcto
    assert "no está activo" in str(excinfo.value).lower()
    # Verificamos que la lista de empleados sigue vacía para proteger la integridad
    assert len(orden.empleados) == 0