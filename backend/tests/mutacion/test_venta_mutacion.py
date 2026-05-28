import pytest
from datetime import datetime, timedelta, timezone
from src.ventas.domain.venta_domain import VentaDomain



def test_mutante_fecha_futura():
    venta = VentaDomain()
    fecha_futura = datetime.now(timezone.utc) + timedelta(days=1)
    with pytest.raises(ValueError):
        venta.inicializar_fecha(fecha_futura)


def test_mutante_cantidad_cero():
    venta = VentaDomain()
    with pytest.raises(ValueError):
        venta.agregar_detalle(producto_id=1, cantidad=0)
