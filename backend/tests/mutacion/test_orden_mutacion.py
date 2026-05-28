import pytest
from datetime import date
from src.ordenes.domain.orden_domain import OrdenDomain



def test_mutante_estado_pago_invalido():
    orden = OrdenDomain()
    with pytest.raises(ValueError):
        orden.inicializar_datos_basicos(garantia=3, estadoPago="pagando", precio=100, fecha=date.today())


def test_mutante_precio_negativo():
    orden = OrdenDomain()
    with pytest.raises(ValueError):
        orden.inicializar_datos_basicos(garantia=3, estadoPago="pendiente", precio=-1, fecha=date.today())
