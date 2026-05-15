"""
Pruebas de Value Object: Cantidad

Tabla de Casos de Prueba:

ID           | Objetivo                      | Escenario (Precondición / Acción)           | Resultado Esperado
-----------  | ----------------------------- | ------------------------------------------- | --------------------------------
CAN-001      | Creación válida               | Crear Cantidad(100)                         | Cantidad se crea exitosamente
CAN-002      | Creación mínima               | Crear Cantidad(1)                           | Cantidad se crea, es_minima=True
CAN-003      | Creación máxima               | Crear Cantidad(10000)                       | Cantidad se crea, es_maxima=True
CAN-004      | Rechazo cero                  | Intentar Cantidad(0)                        | Lanza ValueError
CAN-005      | Rechazo negativo              | Intentar Cantidad(-10)                      | Lanza ValueError
CAN-006      | Rechazo excede límite         | Intentar Cantidad(10001)                    | Lanza ValueError
CAN-007      | Rechazo tipo no entero        | Intentar Cantidad(100.5)                    | Lanza TypeError
CAN-008      | Rechazo tipo string           | Intentar Cantidad("100")                    | Lanza TypeError
CAN-009      | Incrementar válido            | Cantidad(100).incrementar(50)               | Retorna Cantidad(150)
CAN-010      | Incrementar a máximo          | Cantidad(9990).incrementar(10)              | Retorna Cantidad(10000)
CAN-011      | Incrementar excede máximo     | Cantidad(9990).incrementar(20)              | Lanza ValueError
CAN-012      | Decrementar válido            | Cantidad(100).decrementar(50)               | Retorna Cantidad(50)
CAN-013      | Decrementar a mínimo          | Cantidad(10).decrementar(9)                 | Retorna Cantidad(1)
CAN-014      | Decrementar por debajo mínimo | Cantidad(10).decrementar(20)                | Lanza ValueError
CAN-015      | Comparación menor             | Cantidad(50) < Cantidad(100)                | Retorna True
CAN-016      | Comparación mayor             | Cantidad(100) > Cantidad(50)                | Retorna True
CAN-017      | Comparación igual             | Cantidad(100) == Cantidad(100)              | Retorna True
CAN-018      | Igualdad                      | Cantidad(100) == Cantidad(100)              | Son iguales
CAN-019      | Desigualdad                   | Cantidad(100) != Cantidad(50)               | No son iguales
CAN-020      | Rango comercial completo      | Verificar rango [1, 10000]                  | Valores dentro rango válidos

"""
import pytest
from backend.value_objects.cantidad import Cantidad


class TestCantidad:
    """Pruebas para el value object Cantidad"""
    
    def test_cantidad_001_creacion_valida(self):
        """Crear Cantidad con valor válido"""
        cantidad = Cantidad(100)
        assert cantidad.valor == 100
    
    def test_cantidad_002_creacion_minima(self):
        """Crear Cantidad con mínimo permitido"""
        cantidad = Cantidad(1)
        assert cantidad.valor == 1
        assert cantidad.es_minima() is True
    
    def test_cantidad_003_creacion_maxima(self):
        """Crear Cantidad con máximo permitido"""
        cantidad = Cantidad(10000)
        assert cantidad.valor == 10000
        assert cantidad.es_maxima() is True
    
    def test_cantidad_004_rechazo_cero(self):
        """Rechazar Cantidad con valor 0"""
        with pytest.raises(ValueError, match=">= 1"):
            Cantidad(0)
    
    def test_cantidad_005_rechazo_negativo(self):
        """Rechazar Cantidad con valor negativo"""
        with pytest.raises(ValueError):
            Cantidad(-10)
    
    def test_cantidad_006_rechazo_excede_limite(self):
        """Rechazar Cantidad que excede el límite máximo"""
        with pytest.raises(ValueError, match="no puede exceder"):
            Cantidad(10001)
    
    def test_cantidad_007_rechazo_tipo_float(self):
        """Rechazar Cantidad con tipo float"""
        with pytest.raises(TypeError):
            Cantidad(100.5)
    
    def test_cantidad_008_rechazo_tipo_string(self):
        """Rechazar Cantidad con tipo string"""
        with pytest.raises(TypeError):
            Cantidad("100")
    
    def test_cantidad_009_incrementar_valido(self):
        """Incrementar cantidad correctamente"""
        cantidad = Cantidad(100)
        nueva_cantidad = cantidad.incrementar(50)
        assert nueva_cantidad.valor == 150
    
    def test_cantidad_010_incrementar_a_maximo(self):
        """Incrementar cantidad hasta el máximo"""
        cantidad = Cantidad(9990)
        nueva_cantidad = cantidad.incrementar(10)
        assert nueva_cantidad.valor == 10000
    
    def test_cantidad_011_incrementar_excede_maximo(self):
        """Rechazar incremento que excedería el máximo"""
        cantidad = Cantidad(9990)
        with pytest.raises(ValueError):
            cantidad.incrementar(20)
    
    def test_cantidad_012_decrementar_valido(self):
        """Decrementar cantidad correctamente"""
        cantidad = Cantidad(100)
        nueva_cantidad = cantidad.decrementar(50)
        assert nueva_cantidad.valor == 50
    
    def test_cantidad_013_decrementar_a_minimo(self):
        """Decrementar cantidad hasta el mínimo"""
        cantidad = Cantidad(10)
        nueva_cantidad = cantidad.decrementar(9)
        assert nueva_cantidad.valor == 1
    
    def test_cantidad_014_decrementar_por_debajo_minimo(self):
        """Rechazar decremento que estaría por debajo del mínimo"""
        cantidad = Cantidad(10)
        with pytest.raises(ValueError):
            cantidad.decrementar(20)
    
    def test_cantidad_015_comparacion_menor(self):
        """Comparar cantidades: menor que"""
        c1 = Cantidad(50)
        c2 = Cantidad(100)
        assert c1 < c2
    
    def test_cantidad_016_comparacion_mayor(self):
        """Comparar cantidades: mayor que"""
        c1 = Cantidad(100)
        c2 = Cantidad(50)
        assert c1 > c2
    
    def test_cantidad_017_comparacion_igual(self):
        """Comparar cantidades iguales"""
        c1 = Cantidad(100)
        c2 = Cantidad(100)
        assert c1 == c2
    
    def test_cantidad_018_igualdad(self):
        """Dos cantidades iguales son iguales"""
        c1 = Cantidad(100)
        c2 = Cantidad(100)
        assert c1 == c2
    
    def test_cantidad_019_desigualdad(self):
        """Cantidades distintas no son iguales"""
        c1 = Cantidad(100)
        c2 = Cantidad(50)
        assert c1 != c2
    
    def test_cantidad_020_rango_comercial(self):
        """Verificar que el rango comercial es [1, 10000]"""
        # Valores límite válidos
        cantidad_minima = Cantidad(Cantidad.MINIMO)
        cantidad_maxima = Cantidad(Cantidad.MAXIMO)
        assert cantidad_minima.valor == 1
        assert cantidad_maxima.valor == 10000
