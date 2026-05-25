import pytest
from src.servicios.domain.servicio_domain import ServicioDomain

def test_servicio_actualizar_informacion():
    servicio = ServicioDomain()
    
    servicio.actualizar_informacion(
        nombre="Alineación y Balanceo", 
        descripcion="Ajuste completo de la suspensión y llantas"
    )
    
    assert servicio.nombre == "Alineación y Balanceo"
    assert servicio.descripcion == "Ajuste completo de la suspensión y llantas"

def test_servicio_actualizar_informacion_falla():
    servicio = ServicioDomain()
    
    # La descripción es muy corta para el InformacionServicioVO
    with pytest.raises(ValueError, match="al menos 10 caracteres"):
        servicio.actualizar_informacion(nombre="Lava", descripcion="Corta")