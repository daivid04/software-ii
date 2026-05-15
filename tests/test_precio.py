"""
Pruebas de Value Object: Precio

Tabla de Casos de Prueba:

ID           | Objetivo                      | Escenario (Precondición / Acción)           | Resultado Esperado
-----------  | ----------------------------- | ------------------------------------------- | --------------------------------
PRC-001      | Creación válida               | Crear Precio con valor > 0                  | Precio se crea exitosamente
PRC-002      | Creación mínima               | Crear Precio con 0.01                       | Precio se crea exitosamente
PRC-003      | Rechazo cero                  | Intentar asignar Precio 0                   | Lanza ValueError
PRC-004      | Rechazo negativo              | Intentar asignar Precio negativo             | Lanza ValueError
PRC-005      | Validación tipo               | Intentar crear Precio con string            | Lanza TypeError
PRC-006      | Igualdad                      | Comparar dos precios con igual valor        | Son iguales
PRC-007      | Desigualdad                   | Comparar precios con distinto valor         | No son iguales
PRC-008      | Comparación menor             | Comparar p1 < p2 (100 < 200)                | Retorna True
PRC-009      | Comparación mayor             | Comparar p1 > p2 (200 > 100)                | Retorna True
PRC-010      | Comparación menor/igual       | Comparar precios iguales con <=             | Retorna True
PRC-011      | Adición de precios            | Sumar Precio(100) + Precio(50)              | Retorna Precio(150)
PRC-012      | Sustracción válida            | Restar Precio(200) - Precio(50)             | Retorna Precio(150)
PRC-013      | Multiplicación                | Multiplicar Precio(100) * 1.5               | Retorna Precio(150)
PRC-014      | Representación string         | Convertir precio a string                   | Formato: $99.99
PRC-015      | Operaciones inmutables        | Sumar precios sin modificar original         | Original no cambia
"""
import pytest
from backend.value_objects.precio import Precio


class TestPrecio:
    """Pruebas para el value object Precio"""
    
    def test_precio_001_creacion_valida(self):
        """Crear Precio con valor válido > 0"""
        precio = Precio(100.50)
        assert precio.valor == 100.50
    
    def test_precio_002_creacion_minimo(self):
        """Crear Precio con valor mínimo permitido"""
        precio = Precio(0.01)
        assert precio.valor == 0.01
    
    def test_precio_003_rechazo_cero(self):
        """Rechazar Precio con valor 0"""
        with pytest.raises(ValueError, match="mayor a 0"):
            Precio(0)
    
    def test_precio_004_rechazo_negativo(self):
        """Rechazar Precio con valor negativo"""
        with pytest.raises(ValueError, match="no puede ser negativo"):
            Precio(-50)
    
    def test_precio_005_rechazo_tipo_invalido(self):
        """Rechazar Precio con tipo inválido"""
        with pytest.raises(TypeError):
            Precio("100")
    
    def test_precio_006_igualdad(self):
        """Dos precios con igual valor son iguales"""
        p1 = Precio(100)
        p2 = Precio(100)
        assert p1 == p2
    
    def test_precio_007_desigualdad(self):
        """Dos precios con distinto valor no son iguales"""
        p1 = Precio(100)
        p2 = Precio(200)
        assert p1 != p2
    
    def test_precio_008_comparacion_menor(self):
        """Comparar precios: menor que"""
        p1 = Precio(100)
        p2 = Precio(200)
        assert p1 < p2
    
    def test_precio_009_comparacion_mayor(self):
        """Comparar precios: mayor que"""
        p1 = Precio(200)
        p2 = Precio(100)
        assert p1 > p2
    
    def test_precio_010_comparacion_menor_igual(self):
        """Comparar precios: menor o igual"""
        p1 = Precio(100)
        p2 = Precio(100)
        assert p1 <= p2
    
    def test_precio_011_adicion(self):
        """Sumar dos precios"""
        p1 = Precio(100)
        p2 = Precio(50)
        resultado = p1 + p2
        assert resultado == Precio(150)
    
    def test_precio_012_sustraccion_valida(self):
        """Restar precios con resultado válido"""
        p1 = Precio(200)
        p2 = Precio(50)
        resultado = p1 - p2
        assert resultado == Precio(150)
    
    def test_precio_013_multiplicacion(self):
        """Multiplicar precio por factor"""
        p = Precio(100)
        resultado = p * 1.5
        assert resultado == Precio(150)
    
    def test_precio_014_representacion_string(self):
        """Verificar representación en string"""
        p = Precio(99.99)
        assert "$99.99" in str(p)
    
    def test_precio_015_operaciones_no_modifican_original(self):
        """Verificar que operaciones no modifican el original"""
        p = Precio(100)
        p_original = p.valor
        p + Precio(50)
        assert p.valor == p_original
