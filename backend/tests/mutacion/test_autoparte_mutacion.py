import pytest
from src.shared.domain.value_objects import PrecioVO, InventarioVO, CompatibilidadVehiculoVO

def test_mutante_condicion_precio():
    with pytest.raises(ValueError):
        PrecioVO(compra=100.0, venta=80.0)

def test_mutante_calculo_stock_inventario():
    with pytest.raises(ValueError):
        InventarioVO(stock_actual=-1, stock_minimo=0)

def test_mutante_compatibilidad_anio_invalido():
    with pytest.raises(ValueError):
        CompatibilidadVehiculoVO(modelo="AB", anio="xx")
