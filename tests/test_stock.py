"""
Pruebas de Value Object: Stock

Tabla de Casos de Prueba:

ID           | Objetivo                      | Escenario (Precondición / Acción)           | Resultado Esperado
-----------  | ----------------------------- | ------------------------------------------- | --------------------------------
STK-001      | Creación válida               | Crear Stock(100, mín=10)                    | Stock se crea exitosamente
STK-002      | Creación agotado              | Crear Stock(0, mín=5)                       | Stock se crea con cantidad 0
STK-003      | Rechazo cantidad negativa     | Intentar Stock(-10, mín=5)                  | Lanza ValueError
STK-004      | Rechazo mínimo negativo       | Intentar Stock(100, mín=-5)                 | Lanza ValueError
STK-005      | Rechazo tipo no entero        | Intentar Stock(100.5, mín=5)                | Lanza ValueError
STK-006      | Stock bajo - verdadero        | Cantidad(5) < mínimo(10)                    | esta_bajo() = True
STK-007      | Stock bajo - falso            | Cantidad(100) >= mínimo(10)                 | esta_bajo() = False
STK-008      | Disponibilidad suficiente     | Verificar disponibilidad 50 en Stock(100)   | es_disponible(50) = True
STK-009      | Disponibilidad exacta         | Verificar disponibilidad 100 en Stock(100)  | es_disponible(100) = True
STK-010      | Disponibilidad insuficiente   | Verificar disponibilidad 100 en Stock(50)   | es_disponible(100) = False
STK-011      | Reducir válido                | Reducir Stock(100, mín=10) en 30            | Retorna Stock(70, mín=10)
STK-012      | Reducir a cero                | Reducir Stock(50, mín=10) en 50             | Retorna Stock(0, mín=10)
STK-013      | Reducir insuficiente          | Reducir Stock(30) en 50                     | Lanza ValueError
STK-014      | Incrementar válido            | Incrementar Stock(50) en 30                 | Retorna Stock(80, mín=10)
STK-015      | Incrementar desde cero        | Incrementar Stock(0) en 50                  | Retorna Stock(50, mín=10)
STK-016      | Igualdad                      | Comparar Stock(100,10) == Stock(100,10)     | Son iguales
STK-017      | Desigualdad cantidad          | Comparar Stock(100) != Stock(50)            | No son iguales
STK-018      | Operaciones encadenadas       | reducir(20).incrementar(15).reducir(5)      | Resultado correcto = 90
"""
import pytest
from backend.value_objects.stock import Stock


class TestStock:
    """Pruebas para el value object Stock"""
    
    def test_stock_001_creacion_valida(self):
        """Crear Stock con cantidad válida"""
        stock = Stock(cantidad=100, stock_minimo=10)
        assert stock.cantidad == 100
        assert stock.stock_minimo == 10
    
    def test_stock_002_creacion_cero(self):
        """Crear Stock con cantidad 0 (agotado)"""
        stock = Stock(cantidad=0, stock_minimo=5)
        assert stock.cantidad == 0
    
    def test_stock_003_rechazo_cantidad_negativa(self):
        """Rechazar Stock con cantidad negativa"""
        with pytest.raises(ValueError):
            Stock(cantidad=-10, stock_minimo=5)
    
    def test_stock_004_rechazo_minimo_negativo(self):
        """Rechazar Stock con mínimo negativo"""
        with pytest.raises(ValueError):
            Stock(cantidad=100, stock_minimo=-5)
    
    def test_stock_005_rechazo_tipo_invalido_cantidad(self):
        """Rechazar Stock con cantidad no entero"""
        with pytest.raises(ValueError):
            Stock(cantidad=100.5, stock_minimo=5)
    
    def test_stock_006_stock_bajo_verdadero(self):
        """Detectar stock bajo (cantidad < mínimo)"""
        stock = Stock(cantidad=5, stock_minimo=10)
        assert stock.esta_bajo() is True
    
    def test_stock_007_stock_bajo_falso(self):
        """Detectar stock adecuado (cantidad >= mínimo)"""
        stock = Stock(cantidad=100, stock_minimo=10)
        assert stock.esta_bajo() is False
    
    def test_stock_008_disponibilidad_suficiente(self):
        """Verificar disponibilidad: hay suficiente stock"""
        stock = Stock(cantidad=100, stock_minimo=10)
        assert stock.es_disponible(50) is True
    
    def test_stock_009_disponibilidad_exacta(self):
        """Verificar disponibilidad: cantidad exacta"""
        stock = Stock(cantidad=100, stock_minimo=10)
        assert stock.es_disponible(100) is True
    
    def test_stock_010_disponibilidad_insuficiente(self):
        """Verificar disponibilidad: no hay suficiente"""
        stock = Stock(cantidad=50, stock_minimo=10)
        assert stock.es_disponible(100) is False
    
    def test_stock_011_reducir_valido(self):
        """Reducir stock correctamente"""
        stock = Stock(cantidad=100, stock_minimo=10)
        nuevo_stock = stock.reducir(30)
        assert nuevo_stock.cantidad == 70
        assert nuevo_stock.stock_minimo == 10
    
    def test_stock_012_reducir_a_cero(self):
        """Reducir stock hasta agotarse"""
        stock = Stock(cantidad=50, stock_minimo=10)
        nuevo_stock = stock.reducir(50)
        assert nuevo_stock.cantidad == 0
    
    def test_stock_013_reducir_insuficiente(self):
        """Rechazar reducción sin stock suficiente"""
        stock = Stock(cantidad=30, stock_minimo=10)
        with pytest.raises(ValueError, match="No hay suficiente stock"):
            stock.reducir(50)
    
    def test_stock_014_incrementar_valido(self):
        """Incrementar stock correctamente"""
        stock = Stock(cantidad=50, stock_minimo=10)
        nuevo_stock = stock.incrementar(30)
        assert nuevo_stock.cantidad == 80
    
    def test_stock_015_incrementar_cero(self):
        """Incrementar stock desde cero"""
        stock = Stock(cantidad=0, stock_minimo=10)
        nuevo_stock = stock.incrementar(50)
        assert nuevo_stock.cantidad == 50
    
    def test_stock_016_igualdad(self):
        """Dos stocks con iguales valores son iguales"""
        s1 = Stock(cantidad=100, stock_minimo=10)
        s2 = Stock(cantidad=100, stock_minimo=10)
        assert s1 == s2
    
    def test_stock_017_desigualdad_cantidad(self):
        """Stocks con distinta cantidad no son iguales"""
        s1 = Stock(cantidad=100, stock_minimo=10)
        s2 = Stock(cantidad=50, stock_minimo=10)
        assert s1 != s2
    
    def test_stock_018_operaciones_encadenadas(self):
        """Realizar operaciones encadenadas"""
        stock = Stock(cantidad=100, stock_minimo=10)
        resultado = stock.reducir(20).incrementar(15).reducir(5)
        assert resultado.cantidad == 90
