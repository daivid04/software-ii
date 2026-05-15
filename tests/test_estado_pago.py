"""
Pruebas de Value Object: EstadoPago

Tabla de Casos de Prueba:

ID           | Objetivo                      | Escenario (Precondición / Acción)           | Resultado Esperado
-----------  | ----------------------------- | ------------------------------------------- | --------------------------------
EPG-001      | Creación pendiente            | Crear EstadoPago("pendiente")               | Estado es "pendiente"
EPG-002      | Creación parcial              | Crear EstadoPago("parcial")                 | Estado es "parcial"
EPG-003      | Creación completado           | Crear EstadoPago("completado")              | Estado es "completado"
EPG-004      | Rechazo estado inválido       | Intentar EstadoPago("en_proceso")           | Lanza ValueError
EPG-005      | Transición pendiente→parcial  | Transicionar de pendiente a parcial         | Exitoso, nuevo estado es parcial
EPG-006      | Transición pendiente→completado | Transicionar directamente a completado     | Exitoso, nuevo estado es completado
EPG-007      | Transición parcial→completado | Transicionar de parcial a completado        | Exitoso, nuevo estado es completado
EPG-008      | Rechazo transición hacia atrás | Intentar parcial → pendiente                | Lanza ValueError
EPG-009      | Rechazo desde completado      | Intentar transición desde completado        | Lanza ValueError
EPG-010      | Flujo completo                | pendiente → parcial → completado            | Todas las transiciones exitosas
EPG-011      | Igualdad                      | Comparar EstadoPago("pendiente") == ...     | Son iguales
EPG-012      | Desigualdad                   | Comparar EstadoPago("pendiente") != ...     | No son iguales
EPG-013      | Representación string         | Convertir a repr                            | Contiene el estado
"""
import pytest
from backend.value_objects.estado_pago import EstadoPago


class TestEstadoPago:
    """Pruebas para el value object EstadoPago"""
    
    def test_estado_pago_001_creacion_pendiente(self):
        """Crear EstadoPago inicial como pendiente"""
        estado = EstadoPago("pendiente")
        assert estado.estado == "pendiente"
        assert estado.es_pendiente is True
    
    def test_estado_pago_002_creacion_parcial(self):
        """Crear EstadoPago en estado parcial"""
        estado = EstadoPago("parcial")
        assert estado.estado == "parcial"
        assert estado.es_parcial is True
    
    def test_estado_pago_003_creacion_completado(self):
        """Crear EstadoPago en estado completado"""
        estado = EstadoPago("completado")
        assert estado.estado == "completado"
        assert estado.es_completado is True
    
    def test_estado_pago_004_rechazo_estado_invalido(self):
        """Rechazar estado inválido"""
        with pytest.raises(ValueError, match="Estado inválido"):
            EstadoPago("en_proceso")
    
    def test_estado_pago_005_transicion_pendiente_parcial(self):
        """Transicionar pendiente → parcial"""
        estado = EstadoPago("pendiente")
        assert estado.puede_transicionar_a("parcial") is True
        nuevo_estado = estado.transicionar_a("parcial")
        assert nuevo_estado.es_parcial is True
    
    def test_estado_pago_006_transicion_pendiente_completado(self):
        """Transicionar pendiente → completado directamente"""
        estado = EstadoPago("pendiente")
        assert estado.puede_transicionar_a("completado") is True
        nuevo_estado = estado.transicionar_a("completado")
        assert nuevo_estado.es_completado is True
    
    def test_estado_pago_007_transicion_parcial_completado(self):
        """Transicionar parcial → completado"""
        estado = EstadoPago("parcial")
        assert estado.puede_transicionar_a("completado") is True
        nuevo_estado = estado.transicionar_a("completado")
        assert nuevo_estado.es_completado is True
    
    def test_estado_pago_008_transicion_invalida_hacia_atras(self):
        """Rechazar transición hacia atrás (parcial → pendiente)"""
        estado = EstadoPago("parcial")
        assert estado.puede_transicionar_a("pendiente") is False
        with pytest.raises(ValueError, match="Transición inválida"):
            estado.transicionar_a("pendiente")
    
    def test_estado_pago_009_transicion_invalida_completado(self):
        """Rechazar transición desde completado"""
        estado = EstadoPago("completado")
        assert estado.puede_transicionar_a("pendiente") is False
        assert estado.puede_transicionar_a("parcial") is False
    
    def test_estado_pago_010_flujo_completo(self):
        """Recorrer flujo completo: pendiente → parcial → completado"""
        estado = EstadoPago("pendiente")
        assert estado.es_pendiente is True
        
        estado = estado.transicionar_a("parcial")
        assert estado.es_parcial is True
        
        estado = estado.transicionar_a("completado")
        assert estado.es_completado is True
    
    def test_estado_pago_011_igualdad(self):
        """Dos EstadoPago con igual estado son iguales"""
        e1 = EstadoPago("pendiente")
        e2 = EstadoPago("pendiente")
        assert e1 == e2
    
    def test_estado_pago_012_desigualdad(self):
        """EstadoPago con distinto estado no son iguales"""
        e1 = EstadoPago("pendiente")
        e2 = EstadoPago("completado")
        assert e1 != e2
    
    def test_estado_pago_013_representacion_string(self):
        """Verificar representación en string"""
        estado = EstadoPago("pendiente")
        assert "pendiente" in repr(estado)
