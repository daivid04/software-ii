"""
Pruebas de Value Object: Garantia

Tabla de Casos de Prueba:

ID           | Objetivo                      | Escenario (Precondición / Acción)           | Resultado Esperado
-----------  | ----------------------------- | ------------------------------------------- | --------------------------------
GRT-001      | Sin garantía                  | Crear Garantia(0)                           | Garantia se crea, es_sin_garantia=True
GRT-002      | Garantía mínima               | Crear Garantia(1)                           | Garantia se crea exitosamente
GRT-003      | Garantía máxima               | Crear Garantia(10)                          | Garantia se crea exitosamente
GRT-004      | Rechazo negativo              | Intentar Garantia(-1)                       | Lanza ValueError
GRT-005      | Rechazo superior a límite     | Intentar Garantia(15)                       | Lanza ValueError
GRT-006      | Rechazo tipo no entero        | Intentar Garantia(5.5)                      | Lanza TypeError
GRT-007      | Conversión a meses            | Garantia(2).meses                           | Retorna 24
GRT-008      | Conversión a días             | Garantia(1).dias                            | Retorna 365
GRT-009      | No es extendida (< 5)         | Garantia(4).es_extendida                    | Retorna False
GRT-010      | Es extendida (>= 5)           | Garantia(5).es_extendida                    | Retorna True
GRT-011      | Comparación menor             | Garantia(2) < Garantia(5)                   | Retorna True
GRT-012      | Comparación mayor             | Garantia(8) > Garantia(3)                   | Retorna True
GRT-013      | Comparación igual             | Garantia(5) == Garantia(5)                  | Retorna True
GRT-014      | Igualdad                      | Comparar Garantia(3) == Garantia(3)         | Son iguales
GRT-015      | Desigualdad                   | Comparar Garantia(3) != Garantia(5)         | No son iguales
"""
import pytest
from backend.value_objects.garantia import Garantia


class TestGarantia:
    """Pruebas para el value object Garantia"""
    
    def test_garantia_001_sin_garantia(self):
        """Crear Garantia con 0 años (sin garantía)"""
        garantia = Garantia(0)
        assert garantia.anos == 0
        assert garantia.es_sin_garantia is True
    
    def test_garantia_002_garantia_minima(self):
        """Crear Garantia mínima de 1 año"""
        garantia = Garantia(1)
        assert garantia.anos == 1
        assert garantia.es_sin_garantia is False
    
    def test_garantia_003_garantia_maxima(self):
        """Crear Garantia máxima de 10 años"""
        garantia = Garantia(10)
        assert garantia.anos == 10
    
    def test_garantia_004_rechazo_negativo(self):
        """Rechazar garantía negativa"""
        with pytest.raises(ValueError):
            Garantia(-1)
    
    def test_garantia_005_rechazo_superior_limite(self):
        """Rechazar garantía mayor a 10 años"""
        with pytest.raises(ValueError):
            Garantia(15)
    
    def test_garantia_006_rechazo_tipo_invalido(self):
        """Rechazar garantía con tipo no entero"""
        with pytest.raises(TypeError):
            Garantia(5.5)
    
    def test_garantia_007_conversion_meses(self):
        """Convertir años a meses correctamente"""
        garantia = Garantia(2)
        assert garantia.meses == 24
    
    def test_garantia_008_conversion_dias(self):
        """Convertir años a días aproximadamente"""
        garantia = Garantia(1)
        assert garantia.dias == 365
    
    def test_garantia_009_es_extendida_falso(self):
        """Garantía de 4 años no es extendida"""
        garantia = Garantia(4)
        assert garantia.es_extendida is False
    
    def test_garantia_010_es_extendida_verdadero(self):
        """Garantía de 5 o más años es extendida"""
        garantia = Garantia(5)
        assert garantia.es_extendida is True
    
    def test_garantia_011_comparacion_menor(self):
        """Comparar garantías: menor que"""
        g1 = Garantia(2)
        g2 = Garantia(5)
        assert g1 < g2
    
    def test_garantia_012_comparacion_mayor(self):
        """Comparar garantías: mayor que"""
        g1 = Garantia(8)
        g2 = Garantia(3)
        assert g1 > g2
    
    def test_garantia_013_comparacion_igual(self):
        """Comparar garantías iguales"""
        g1 = Garantia(5)
        g2 = Garantia(5)
        assert g1 == g2
    
    def test_garantia_014_igualdad(self):
        """Dos garantías con igual años son iguales"""
        g1 = Garantia(3)
        g2 = Garantia(3)
        assert g1 == g2
    
    def test_garantia_015_desigualdad(self):
        """Garantías con distinto años no son iguales"""
        g1 = Garantia(3)
        g2 = Garantia(5)
        assert g1 != g2
