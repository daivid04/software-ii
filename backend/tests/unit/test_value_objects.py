import pytest
from datetime import datetime, timezone, timedelta
from dataclasses import FrozenInstanceError

# Asegúrate de que esta ruta apunte correctamente a donde están tus VOs
from src.shared.domain.value_objects import (
    PrecioVO, InventarioVO, CompatibilidadVehiculoVO, CantidadVentaVO,
    FechaVentaVO, InformacionServicioVO, InformacionEmpleadoVO,
    EstadoEmpleadoVO, GarantiaVO, EstadoPagoVO, PrecioOrdenVO
)

# ==========================================
# 1. PRUEBAS DE REGLAS DE ORO DEL DOMINIO (Rúbrica: Inmutabilidad y Comparación)
# ==========================================

def test_value_objects_son_inmutables():
    """Prueba que un VO no puede ser modificado después de instanciado (Frozen)"""
    precio = PrecioVO(compra=100.0, venta=150.0)
    with pytest.raises(FrozenInstanceError):
        precio.compra = 90.0  # Intentar hackear el precio debe fallar

def test_value_objects_comparacion_por_atributos():
    """Prueba que dos VOs distintos en memoria pero con mismos datos son iguales"""
    precio1 = PrecioVO(compra=100.0, venta=150.0)
    precio2 = PrecioVO(compra=100.0, venta=150.0)
    assert precio1 == precio2  # Igualdad matemática

# ==========================================
# 2. PRUEBAS DE VALIDACIÓN DE CADA VALUE OBJECT
# ==========================================

# --- PrecioVO ---
def test_precio_vo_valido():
    precio = PrecioVO(compra=100, venta=150)
    assert precio.compra == 100
    assert precio.venta == 150

def test_precio_vo_negativo():
    with pytest.raises(ValueError, match="Los precios no pueden ser negativos"):
        PrecioVO(compra=-10, venta=50)

def test_precio_vo_venta_menor_compra():
    with pytest.raises(ValueError, match="El precio de venta debe ser mayor al precio de compra"):
        PrecioVO(compra=100, venta=90)

# --- InventarioVO ---
def test_inventario_vo_valido():
    inv = InventarioVO(stock_actual=10, stock_minimo=5)
    assert inv.stock_actual == 10

def test_inventario_vo_negativo():
    with pytest.raises(ValueError, match="El stock no puede ser negativo"):
        InventarioVO(stock_actual=-5, stock_minimo=2)

def test_inventario_vo_despachar_exito():
    inv = InventarioVO(stock_actual=10, stock_minimo=5)
    nuevo_inv = inv.despachar(3)
    assert nuevo_inv.stock_actual == 7  # Retorna un nuevo VO con el cálculo

def test_inventario_vo_despachar_sin_stock():
    inv = InventarioVO(stock_actual=10, stock_minimo=5)
    with pytest.raises(ValueError, match="Stock insuficiente para despachar"):
        inv.despachar(15)

# --- CompatibilidadVehiculoVO ---
def test_compatibilidad_vo_valido():
    comp = CompatibilidadVehiculoVO(modelo="Corolla", anio="2020-2023")
    assert comp.modelo == "Corolla"

def test_compatibilidad_vo_modelo_invalido():
    with pytest.raises(ValueError, match="El modelo del vehículo debe tener al menos 2 caracteres"):
        CompatibilidadVehiculoVO(modelo="A", anio="2020")

def test_compatibilidad_vo_anio_invalido():
    with pytest.raises(ValueError, match="contener al menos un año válido"):
        CompatibilidadVehiculoVO(modelo="Corolla", anio="dos mil veinte")

# --- CantidadVentaVO ---
def test_cantidad_venta_vo_invalida():
    with pytest.raises(ValueError, match="mayor a cero"):
        CantidadVentaVO(0)

# --- FechaVentaVO ---
def test_fecha_venta_vo_pasada():
    hace_una_hora = datetime.now(timezone.utc) - timedelta(hours=1)
    fecha = FechaVentaVO(hace_una_hora)
    assert fecha.valor == hace_una_hora

def test_fecha_venta_vo_futura():
    manana = datetime.now(timezone.utc) + timedelta(days=1)
    with pytest.raises(ValueError, match="La fecha de la venta no puede ser una fecha futura"):
        FechaVentaVO(manana)

# --- InformacionServicioVO ---
def test_info_servicio_vo_invalida():
    with pytest.raises(ValueError, match="al menos 10 caracteres"):
        InformacionServicioVO(nombre="Filtro", descripcion="Cortita")

# --- InformacionEmpleadoVO ---
def test_info_empleado_vo_invalida():
    with pytest.raises(ValueError, match="nombres deben tener al menos 2 caracteres"):
        InformacionEmpleadoVO(nombres="A", apellidos="Perez", especialidad="Motor")

# --- EstadoEmpleadoVO ---
def test_estado_empleado_vo_valido():
    estado = EstadoEmpleadoVO("VACACIONES")
    assert estado.valor == "VACACIONES" # Tu VO no hace .lower() a sí mismo, sino en el parent

def test_estado_empleado_vo_invalido():
    with pytest.raises(ValueError, match="Estado de empleado no válido"):
        EstadoEmpleadoVO("despedido")

# --- GarantiaVO ---
def test_garantia_vo_invalida():
    with pytest.raises(ValueError, match="negativo"):
        GarantiaVO(-1)

# --- EstadoPagoVO ---
def test_estado_pago_vo_invalido():
    with pytest.raises(ValueError, match="Estado de pago inválido"):
        EstadoPagoVO("fiado")

# --- PrecioOrdenVO ---
def test_precio_orden_vo_invalido():
    with pytest.raises(ValueError, match="negativo"):
        PrecioOrdenVO(-50)