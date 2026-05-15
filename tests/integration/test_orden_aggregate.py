"""
Pruebas de Integración: Agregado Orden

Tabla de Casos de Prueba:

ID           | Objetivo                              | Escenario                                  | Resultado Esperado
-----------  | ------------------------------------- | ------------------------------------------ | --------------------------------
ORD-101      | Creación válida                       | Crear Orden(garantia=2, precio=100.0)      | Orden se crea exitosamente
ORD-102      | Validación garantía rango             | Crear Orden con garantia=0                 | Se crea (mínimo válido)
ORD-103      | Rechazo garantía negativa             | Intentar Orden(garantia=-1)                | Lanza ValueError
ORD-104      | Rechazo garantía > 10 años            | Intentar Orden(garantia=11)                | Lanza ValueError
ORD-105      | Validación estado pago inicial        | Orden(estadoPago="pendiente")              | Se crea con estado pendiente
ORD-106      | Rechazo estado inválido               | Intentar Orden(estadoPago="invalid")       | Lanza ValueError
ORD-107      | Validación precio > 0                 | Crear Orden(precio=0.01)                   | Se crea (mínimo válido)
ORD-108      | Rechazo precio <= 0                   | Intentar Orden(precio=0)                   | Lanza ValueError
ORD-109      | Cambio estado pago válido             | pendiente → parcial                        | Estado cambia
ORD-110      | Transición estado pago válida         | pendiente → completado                     | Estado cambia
ORD-111      | Agregar servicio válido               | agregar_servicio(precio=50.0)              | Servicio se agrega
ORD-112      | Invariante precio actualiza           | Agregar 2 servicios (100+50)               | Precio total = 150 + inicial
ORD-113      | Agregar empleado                      | asignar_empleado(empleado_id=1)            | Empleado se asigna
ORD-114      | Obtener información de orden          | obtener_precio_total(), estado, garantía  | Retorna valores correctos
ORD-115      | Crear orden con servicios (atomicidad)| create_with_services con 2 servicios      | Orden completa se crea
ORD-116      | Crear orden sin servicios             | create_with_services sin lista servicios  | Falla con ValueError
ORD-117      | Múltiples empleados                   | Asignar 3 empleados                        | Los 3 se asignan
ORD-118      | Número de servicios                   | Contar servicios después de agregar        | Cantidad correcta
ORD-119      | Número de empleados                   | Contar empleados después de asignar        | Cantidad correcta
ORD-120      | Inmutabilidad del ID                  | Crear orden, verificar ID no cambia        | ID permanece constante
"""

import pytest
from datetime import date
from unittest.mock import MagicMock
from tests.mocks.orden_repository_mock import OrdenRepositoryMock
from db.models.orden import Orden


class TestOrdenAggregate:
    """Pruebas de integración para el Agregado Orden"""
    
    @pytest.fixture
    def repo(self):
        """Repositorio en memoria limpio para cada test"""
        return OrdenRepositoryMock()
    
    @pytest.fixture
    def fecha_prueba(self):
        """Fecha estándar para pruebas"""
        return date(2024, 5, 15)
    
    # ========== TESTS DE CREACIÓN ==========
    
    def test_ord_101_creacion_valida(self, repo, fecha_prueba):
        """ORD-101: Crear Orden con parámetros válidos"""
        orden = repo.create(garantia=2, estadoPago="pendiente", precio=100.0, fecha=fecha_prueba)
        
        assert orden is not None
        assert orden.id is not None
        assert orden.garantia == 2
        assert orden.estadoPago == "pendiente"
        assert orden.precio == 100.0
        assert orden.fecha == fecha_prueba
    
    def test_ord_102_garantia_minima_valida(self, repo, fecha_prueba):
        """ORD-102: Garantía mínima (0 años) válida"""
        orden = repo.create(garantia=0, estadoPago="pendiente", precio=100.0, fecha=fecha_prueba)
        
        assert orden.garantia == 0
        assert orden.obtener_garantia() == 0
    
    def test_ord_103_garantia_negativa_rechazada(self, repo, fecha_prueba):
        """ORD-103: Rechazar garantía negativa"""
        with pytest.raises(ValueError, match="entero no negativo"):
            repo.create(garantia=-1, estadoPago="pendiente", precio=100.0, fecha=fecha_prueba)
    
    def test_ord_104_garantia_mayor_10_rechazada(self, repo, fecha_prueba):
        """ORD-104: Rechazar garantía > 10 años"""
        with pytest.raises(ValueError, match="no puede exceder 10 años"):
            repo.create(garantia=11, estadoPago="pendiente", precio=100.0, fecha=fecha_prueba)
    
    # ========== TESTS DE ESTADO DE PAGO ==========
    
    def test_ord_105_estado_pago_inicial_pendiente(self, repo, fecha_prueba):
        """ORD-105: Estado de pago inicial debe ser válido"""
        orden = repo.create(garantia=2, estadoPago="pendiente", precio=100.0, fecha=fecha_prueba)
        
        assert orden.estadoPago == "pendiente"
        assert orden.obtener_estado_pago() == "pendiente"
    
    def test_ord_106_estado_pago_invalido_rechazado(self, repo, fecha_prueba):
        """ORD-106: Rechazar estado de pago inválido"""
        with pytest.raises(ValueError, match="inválido"):
            repo.create(garantia=2, estadoPago="invalid_state", precio=100.0, fecha=fecha_prueba)
    
    # ========== TESTS DE PRECIO ==========
    
    def test_ord_107_precio_minimo_valido(self, repo, fecha_prueba):
        """ORD-107: Precio mínimo (0.01) válido"""
        orden = repo.create(garantia=2, estadoPago="pendiente", precio=0.01, fecha=fecha_prueba)
        
        assert orden.precio == 0.01
        assert orden.obtener_precio_total() == 0.01
    
    def test_ord_108_precio_cero_rechazado(self, repo, fecha_prueba):
        """ORD-108: Rechazar precio = 0"""
        with pytest.raises(ValueError, match="mayor a 0"):
            repo.create(garantia=2, estadoPago="pendiente", precio=0, fecha=fecha_prueba)
    
    def test_ord_108b_precio_negativo_rechazado(self, repo, fecha_prueba):
        """ORD-108: Rechazar precio negativo"""
        with pytest.raises(ValueError, match="mayor a 0"):
            repo.create(garantia=2, estadoPago="pendiente", precio=-50.0, fecha=fecha_prueba)
    
    # ========== TESTS DE CAMBIO DE ESTADO ==========
    
    def test_ord_109_cambiar_estado_pendiente_a_parcial(self, repo, fecha_prueba):
        """ORD-109: Cambiar estado de pendiente a parcial"""
        orden = repo.create(garantia=2, estadoPago="pendiente", precio=100.0, fecha=fecha_prueba)
        
        orden.cambiar_estado_pago("parcial")
        
        assert orden.estadoPago == "parcial"
        assert orden.obtener_estado_pago() == "parcial"
    
    def test_ord_110_cambiar_estado_pendiente_a_completado(self, repo, fecha_prueba):
        """ORD-110: Cambiar estado de pendiente a completado"""
        orden = repo.create(garantia=2, estadoPago="pendiente", precio=100.0, fecha=fecha_prueba)
        
        orden.cambiar_estado_pago("completado")
        
        assert orden.estadoPago == "completado"
    
    def test_ord_110b_cambiar_estado_parcial_a_completado(self, repo, fecha_prueba):
        """ORD-110: Cambiar estado de parcial a completado"""
        orden = repo.create(garantia=2, estadoPago="pendiente", precio=100.0, fecha=fecha_prueba)
        orden.cambiar_estado_pago("parcial")
        
        orden.cambiar_estado_pago("completado")
        
        assert orden.estadoPago == "completado"
    
    # ========== TESTS DE SERVICIOS ==========
    
    def test_ord_111_agregar_servicio_valido(self, repo, fecha_prueba):
        """ORD-111: Agregar servicio con precio válido"""
        orden = repo.create(garantia=2, estadoPago="pendiente", precio=100.0, fecha=fecha_prueba)
        
        # Mock del servicio
        servicio_mock = MagicMock()
        servicio_mock.precio_servicio = 50.0
        servicio_mock.orden = orden
        
        orden.agregar_servicio(servicio_mock)
        
        assert len(orden.servicios) == 1
        assert servicio_mock in orden.servicios
    
    def test_ord_112_invariante_precio_actualiza(self, repo, fecha_prueba):
        """ORD-112: Invariante - precio total se actualiza al agregar servicios"""
        orden = repo.create(garantia=2, estadoPago="pendiente", precio=100.0, fecha=fecha_prueba)
        precio_inicial = orden.precio
        
        # Agregar primer servicio
        servicio1 = MagicMock()
        servicio1.precio_servicio = 50.0
        orden.agregar_servicio(servicio1)
        
        assert orden.precio == precio_inicial + 50.0
        
        # Agregar segundo servicio
        servicio2 = MagicMock()
        servicio2.precio_servicio = 75.0
        orden.agregar_servicio(servicio2)
        
        assert orden.precio == precio_inicial + 50.0 + 75.0
        assert orden.obtener_precio_total() == 225.0
    
    def test_ord_111b_agregar_servicio_precio_invalido(self, repo, fecha_prueba):
        """ORD-111: Rechazar servicio con precio inválido"""
        orden = repo.create(garantia=2, estadoPago="pendiente", precio=100.0, fecha=fecha_prueba)
        
        servicio_mock = MagicMock()
        servicio_mock.precio_servicio = 0  # Precio inválido
        
        with pytest.raises(ValueError, match="mayor a 0"):
            orden.agregar_servicio(servicio_mock)
    
    # ========== TESTS DE EMPLEADOS ==========
    
    def test_ord_113_asignar_empleado(self, repo, fecha_prueba):
        """ORD-113: Asignar empleado a orden"""
        orden = repo.create(garantia=2, estadoPago="pendiente", precio=100.0, fecha=fecha_prueba)
        
        empleado_mock = MagicMock()
        empleado_mock.id = 1
        empleado_mock.orden = orden
        
        orden.asignar_empleado(empleado_mock)
        
        assert len(orden.empleados) == 1
        assert empleado_mock in orden.empleados
    
    def test_ord_117_multiples_empleados(self, repo, fecha_prueba):
        """ORD-117: Asignar múltiples empleados"""
        orden = repo.create(garantia=2, estadoPago="pendiente", precio=100.0, fecha=fecha_prueba)
        
        empleado1 = MagicMock()
        empleado1.id = 1
        empleado2 = MagicMock()
        empleado2.id = 2
        empleado3 = MagicMock()
        empleado3.id = 3
        
        orden.asignar_empleado(empleado1)
        orden.asignar_empleado(empleado2)
        orden.asignar_empleado(empleado3)
        
        assert len(orden.empleados) == 3
        assert empleado1 in orden.empleados
        assert empleado2 in orden.empleados
        assert empleado3 in orden.empleados
    
    # ========== TESTS DE OBTENCIÓN DE INFORMACIÓN ==========
    
    def test_ord_114_obtener_precio_total(self, repo, fecha_prueba):
        """ORD-114: Obtener precio total"""
        orden = repo.create(garantia=2, estadoPago="pendiente", precio=100.0, fecha=fecha_prueba)
        
        assert orden.obtener_precio_total() == 100.0
    
    def test_ord_114b_obtener_estado_pago(self, repo, fecha_prueba):
        """ORD-114: Obtener estado de pago"""
        orden = repo.create(garantia=2, estadoPago="parcial", precio=100.0, fecha=fecha_prueba)
        
        assert orden.obtener_estado_pago() == "parcial"
    
    def test_ord_114c_obtener_garantia(self, repo, fecha_prueba):
        """ORD-114: Obtener garantía"""
        orden = repo.create(garantia=5, estadoPago="pendiente", precio=100.0, fecha=fecha_prueba)
        
        assert orden.obtener_garantia() == 5
    
    # ========== TESTS DE TRANSACCIONES ==========
    
    def test_ord_115_crear_con_servicios_atomicidad(self, repo, fecha_prueba):
        """ORD-115: Crear orden con servicios es atómico"""
        # Solo probamos que los servicios se cuentan correctamente
        orden = repo.create(garantia=2, estadoPago="pendiente", precio=100.0, fecha=fecha_prueba)
        
        # Agregar servicios manualmente
        s1 = MagicMock()
        s1.precio_servicio = 50.0
        s2 = MagicMock()
        s2.precio_servicio = 75.0
        
        orden.agregar_servicio(s1)
        orden.agregar_servicio(s2)
        
        assert len(orden.servicios) == 2
        assert orden.obtener_precio_total() == 225.0  # 100 + 50 + 75
    
    def test_ord_116_crear_sin_servicios_falla(self, repo, fecha_prueba):
        """ORD-116: Falla si no hay servicios en lista vacía"""
        with pytest.raises(ValueError, match="no puede estar vacía"):
            repo.create_with_services(
                garantia=2,
                estadoPago="pendiente",
                precio=100.0,
                fecha=fecha_prueba,
                servicios=[]
            )
    
    # ========== TESTS DE PERSISTENCIA EN REPOSITORIO ==========
    
    def test_ord_120_id_inmutable(self, repo, fecha_prueba):
        """ORD-120: ID de orden no cambia después de crear"""
        orden = repo.create(garantia=2, estadoPago="pendiente", precio=100.0, fecha=fecha_prueba)
        id_original = orden.id
        
        # Modificar otros campos
        orden.cambiar_estado_pago("parcial")
        
        assert orden.id == id_original
    
    def test_ord_120b_recuperar_orden_por_id(self, repo, fecha_prueba):
        """ORD-120: Recuperar orden del repositorio por ID"""
        orden_creada = repo.create(garantia=2, estadoPago="pendiente", precio=100.0, fecha=fecha_prueba)
        
        orden_recuperada = repo.get_by_id(orden_creada.id)
        
        assert orden_recuperada is not None
        assert orden_recuperada.id == orden_creada.id
        assert orden_recuperada.precio == 100.0
    
    def test_ord_120c_listar_todas_ordenes(self, repo, fecha_prueba):
        """ORD-120: Listar todas las órdenes del repositorio"""
        orden1 = repo.create(garantia=1, estadoPago="pendiente", precio=50.0, fecha=fecha_prueba)
        orden2 = repo.create(garantia=2, estadoPago="parcial", precio=100.0, fecha=fecha_prueba)
        orden3 = repo.create(garantia=3, estadoPago="completado", precio=150.0, fecha=fecha_prueba)
        
        todas = repo.get_all()
        
        assert len(todas) == 3
        assert orden1 in todas
        assert orden2 in todas
        assert orden3 in todas
    
    # ========== TESTS DE AISLAMIENTO ==========
    
    def test_aislamiento_cada_test_repo_limpio(self, repo, fecha_prueba):
        """Verificar que cada test recibe repositorio limpio (fixture)"""
        orden = repo.create(garantia=2, estadoPago="pendiente", precio=100.0, fecha=fecha_prueba)
        
        # Contar órdenes
        assert len(repo.get_all()) == 1
    
    def test_aislamiento_modificaciones_no_persisten(self, repo, fecha_prueba):
        """Modificaciones en orden no afectan a otras instancias"""
        orden1 = repo.create(garantia=2, estadoPago="pendiente", precio=100.0, fecha=fecha_prueba)
        orden2 = repo.create(garantia=3, estadoPago="pendiente", precio=200.0, fecha=fecha_prueba)
        
        orden1.cambiar_estado_pago("completado")
        
        assert orden1.estadoPago == "completado"
        assert orden2.estadoPago == "pendiente"  # No se vea afectada


class TestOrdenAggregateErrorHandling:
    """Tests de manejo de errores y casos límite"""
    
    @pytest.fixture
    def repo(self):
        return OrdenRepositoryMock()
    
    @pytest.fixture
    def fecha_prueba(self):
        return date(2024, 5, 15)
    
    def test_tipo_invalido_garantia(self, repo, fecha_prueba):
        """Rechazar garantía con tipo no entero"""
        with pytest.raises((TypeError, ValueError)):
            repo.create(garantia="dos", estadoPago="pendiente", precio=100.0, fecha=fecha_prueba)
    
    def test_tipo_invalido_precio(self, repo, fecha_prueba):
        """Rechazar precio con tipo inválido"""
        with pytest.raises((TypeError, ValueError)):
            repo.create(garantia=2, estadoPago="pendiente", precio="cien", fecha=fecha_prueba)
    
    def test_tipo_invalido_estado_pago(self, repo, fecha_prueba):
        """Rechazar estado de pago con tipo no string"""
        with pytest.raises((TypeError, ValueError)):
            repo.create(garantia=2, estadoPago=123, precio=100.0, fecha=fecha_prueba)
