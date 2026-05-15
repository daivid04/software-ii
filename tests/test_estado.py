"""
Pruebas de Value Object: Estado

Tabla de Casos de Prueba:

ID           | Objetivo                      | Escenario (Precondición / Acción)           | Resultado Esperado
-----------  | ----------------------------- | ------------------------------------------- | --------------------------------
EST-001      | Crear activo                  | Crear Estado("activo")                      | Se crea, es_activo=True
EST-002      | Crear inactivo                | Crear Estado("inactivo")                    | Se crea, es_inactivo=True
EST-003      | Crear licencia                | Crear Estado("licencia")                    | Se crea exitosamente
EST-004      | Crear suspendido              | Crear Estado("suspendido")                  | Se crea exitosamente
EST-005      | Normalizar mayúsculas         | Estado("ACTIVO")                            | Normalizado a minúsculas
EST-006      | Normalizar espacios           | Estado("  inactivo  ")                      | Espacios eliminados
EST-007      | Rechazo estado inválido       | Intentar Estado("desconocido")              | Lanza ValueError
EST-008      | Rechazo tipo no string        | Intentar Estado(123)                        | Lanza TypeError
EST-009      | Puede trabajar - activo       | Estado("activo").puede_trabajar             | Retorna True
EST-010      | Puede trabajar - licencia     | Estado("licencia").puede_trabajar           | Retorna True
EST-011      | No puede trabajar - inactivo  | Estado("inactivo").puede_trabajar           | Retorna False
EST-012      | No puede trabajar - suspendido| Estado("suspendido").puede_trabajar         | Retorna False
EST-013      | Cambiar de estado             | Estado("activo").cambiar_a("licencia")     | Retorna nuevo Estado
EST-014      | Cambio preserva original      | Cambio no modifica el estado original        | Original se mantiene
EST-015      | Igualdad                      | Estado("activo") == Estado("activo")        | Son iguales
EST-016      | Desigualdad                   | Estado("activo") != Estado("inactivo")      | No son iguales
EST-017      | Representación string         | repr(Estado("licencia"))                    | Contiene "licencia"
EST-018      | Todos los estados             | Crear los 4 estados válidos                 | Todos se crean exitosamente
"""
import pytest
from backend.value_objects.estado import Estado


class TestEstado:
    """Pruebas para el value object Estado"""
    
    def test_estado_001_creacion_activo(self):
        """Crear Estado activo"""
        estado = Estado("activo")
        assert estado.nombre == "activo"
        assert estado.es_activo is True
    
    def test_estado_002_creacion_inactivo(self):
        """Crear Estado inactivo"""
        estado = Estado("inactivo")
        assert estado.nombre == "inactivo"
        assert estado.es_inactivo is True
    
    def test_estado_003_creacion_licencia(self):
        """Crear Estado en licencia"""
        estado = Estado("licencia")
        assert estado.nombre == "licencia"
    
    def test_estado_004_creacion_suspendido(self):
        """Crear Estado suspendido"""
        estado = Estado("suspendido")
        assert estado.nombre == "suspendido"
    
    def test_estado_005_normalizacion_mayusculas(self):
        """Normalizar Estado a minúsculas"""
        estado = Estado("ACTIVO")
        assert estado.nombre == "activo"
    
    def test_estado_006_normalizacion_espacios(self):
        """Eliminar espacios en blanco"""
        estado = Estado("  inactivo  ")
        assert estado.nombre == "inactivo"
    
    def test_estado_007_rechazo_invalido(self):
        """Rechazar estado inválido"""
        with pytest.raises(ValueError, match="Estado inválido"):
            Estado("desconocido")
    
    def test_estado_008_rechazo_tipo_invalido(self):
        """Rechazar estado con tipo no string"""
        with pytest.raises(TypeError):
            Estado(123)
    
    def test_estado_009_puede_trabajar_activo(self):
        """Empleado activo puede trabajar"""
        estado = Estado("activo")
        assert estado.puede_trabajar is True
    
    def test_estado_010_puede_trabajar_licencia(self):
        """Empleado en licencia puede trabajar"""
        estado = Estado("licencia")
        assert estado.puede_trabajar is True
    
    def test_estado_011_puede_trabajar_inactivo(self):
        """Empleado inactivo NO puede trabajar"""
        estado = Estado("inactivo")
        assert estado.puede_trabajar is False
    
    def test_estado_012_puede_trabajar_suspendido(self):
        """Empleado suspendido NO puede trabajar"""
        estado = Estado("suspendido")
        assert estado.puede_trabajar is False
    
    def test_estado_013_cambiar_a_nuevo_estado(self):
        """Cambiar de un estado a otro"""
        estado = Estado("activo")
        nuevo_estado = estado.cambiar_a("licencia")
        assert nuevo_estado.nombre == "licencia"
    
    def test_estado_014_cambio_preserva_inmutabilidad(self):
        """Cambio de estado no modifica el anterior"""
        estado1 = Estado("activo")
        estado2 = estado1.cambiar_a("inactivo")
        assert estado1.nombre == "activo"
        assert estado2.nombre == "inactivo"
    
    def test_estado_015_igualdad(self):
        """Dos estados iguales son iguales"""
        e1 = Estado("activo")
        e2 = Estado("activo")
        assert e1 == e2
    
    def test_estado_016_desigualdad(self):
        """Estados distintos no son iguales"""
        e1 = Estado("activo")
        e2 = Estado("inactivo")
        assert e1 != e2
    
    def test_estado_017_representacion_string(self):
        """Verificar representación en string"""
        estado = Estado("licencia")
        assert "licencia" in repr(estado)
    
    def test_estado_018_todos_estados_validos(self):
        """Crear todos los estados válidos"""
        estados_validos = ["activo", "inactivo", "licencia", "suspendido"]
        for estado_nombre in estados_validos:
            estado = Estado(estado_nombre)
            assert estado.nombre == estado_nombre
