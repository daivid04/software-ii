import pytest
from datetime import datetime, timezone, timedelta
from src.ventas.domain.venta_domain import VentaDomain

def test_venta_inicializar_fecha():
    venta = VentaDomain()
    ahora = datetime.now(timezone.utc)

    venta.inicializar_fecha(ahora)
    assert venta.fecha == ahora

def test_venta_inicializar_fecha_futura_falla():
    venta = VentaDomain()
    futuro = datetime.now(timezone.utc) + timedelta(days=5)

    with pytest.raises(ValueError, match="fecha futura"):
        venta.inicializar_fecha(futuro)

def test_venta_agregar_detalle():
    venta = VentaDomain()

    venta.agregar_detalle(producto_id=10, cantidad=2)
    venta.agregar_detalle(producto_id=15, cantidad=1)

    assert len(venta.productos) == 2
    assert venta.productos[0]["producto_id"] == 10
    assert venta.productos[0]["cantidad"] == 2


def test_venta_agregar_detalle_cantidad_cero_falla():
    venta = VentaDomain()
    with pytest.raises(ValueError, match="mayor a cero"):
        venta.agregar_detalle(producto_id=10, cantidad=0)
