import pytest
from src.shared.domain.value_objects import InformacionEmpleadoVO, EstadoEmpleadoVO

def test_mutante_superviviente_cambio_estado():
    with pytest.raises(ValueError):
        EstadoEmpleadoVO(valor="temporal")

def test_mutante_condicion_limite_especialidad():
    with pytest.raises(ValueError):
        InformacionEmpleadoVO(nombres="A", apellidos="Ruiz", especialidad="")
