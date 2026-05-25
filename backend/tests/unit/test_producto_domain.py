import pytest
from src.producto.domain.producto_domain import ProductoDomain

# Función auxiliar para instanciar rápido en las pruebas
def instanciar_producto():
    return ProductoDomain(
        id=1, nombre="Test", descripcion="Test Desc", marca="Test Marca", 
        categoria="Test Cat", precio_compra=0.0, precio_venta=0.0, 
        stock=0, stock_minimo=0, codigo_barras=None, img=None, tipo="producto"
    )

def test_producto_actualizar_informacion_basica():
    producto = instanciar_producto()
    producto.actualizar_informacion_basica("Filtro de Aire", "Filtro premium", "Bosch", "Filtros")
    
    assert producto.nombre == "Filtro de Aire"
    assert producto.marca == "Bosch"

def test_producto_actualizar_informacion_falla_sin_nombre():
    producto = instanciar_producto()
    with pytest.raises(ValueError, match="Nombre y marca son obligatorios"):
        producto.actualizar_informacion_basica("", "Filtro premium", "Bosch", "Filtros")

def test_producto_establecer_precios():
    producto = instanciar_producto()
    producto.establecer_precios(compra=50.0, venta=80.0)
    
    assert producto.precio_compra == 50.0
    assert producto.precio_venta == 80.0

def test_producto_ajustar_inventario():
    producto = instanciar_producto()
    producto.ajustar_inventario(actual=20, minimo=5)
    
    assert producto.stock == 20
    assert producto.stock_minimo == 5

def test_producto_registrar_despacho_exito():
    producto = instanciar_producto()
    producto.ajustar_inventario(actual=10, minimo=2)
    
    producto.registrar_despacho(cantidad=3)
    assert producto.stock == 7

def test_producto_registrar_despacho_falla_sin_stock():
    producto = instanciar_producto()
    producto.ajustar_inventario(actual=2, minimo=1)
    
    with pytest.raises(ValueError, match="Stock insuficiente"):
        producto.registrar_despacho(cantidad=5)