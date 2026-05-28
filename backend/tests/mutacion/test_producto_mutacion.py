import pytest
from src.shared.domain.value_objects import PrecioVO, InventarioVO



def test_mutante_precio_venta_menor_compra():
    with pytest.raises(ValueError):
        PrecioVO(compra=100.0, venta=90.0)


def test_mutante_stock_negativo():
    with pytest.raises(ValueError):
        InventarioVO(stock_actual=-5, stock_minimo=0)
