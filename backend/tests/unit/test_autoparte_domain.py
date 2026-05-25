import pytest
from src.autopartes.domain.autoparte_domain import AutoparteDomain

def instanciar_autoparte():
    return AutoparteDomain(
        id=1, nombre="Bujía", descripcion="Desc", marca="NGK", 
        categoria="Eléctrico", precio_compra=0.0, precio_venta=0.0, 
        stock=0, stock_minimo=0, codigo_barras=None, img=None, tipo="autoparte",
        modelo="", anio=""
    )

def test_autoparte_asignar_compatibilidad():
    autoparte = instanciar_autoparte()
    
    # Este método dispara internamente el CompatibilidadVehiculoVO
    autoparte.asignar_compatibilidad(modelo="Nissan Sentra", anio="2018-2022")
    
    assert autoparte.modelo == "Nissan Sentra"
    assert autoparte.anio == "2018-2022"

def test_autoparte_asignar_compatibilidad_invalida():
    autoparte = instanciar_autoparte()
    
    # El VO debe atrapar este error porque falta el modelo
    with pytest.raises(ValueError, match="al menos 2 caracteres"):
        autoparte.asignar_compatibilidad(modelo="A", anio="2020")