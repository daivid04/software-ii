import pytest
from src.shared.domain.value_objects import InformacionServicioVO



def test_mutante_descripcion_corta():
    with pytest.raises(ValueError):
        InformacionServicioVO(nombre="Ajuste", descripcion="Corto")
