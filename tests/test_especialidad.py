"""
Pruebas de Value Object: Especialidad

Tabla de Casos de Prueba:

ID           | Objetivo                      | Escenario (Precondición / Acción)           | Resultado Esperado
-----------  | ----------------------------- | ------------------------------------------- | --------------------------------
ESP-001      | Crear mecánica                | Crear Especialidad("mecanica")              | Se crea, es_mecanica=True
ESP-002      | Crear electricidad            | Crear Especialidad("electricidad")          | Se crea, es_electricidad=True
ESP-003      | Crear sistemas                | Crear Especialidad("sistemas")              | Se crea, es_sistemas=True
ESP-004      | Normalizar mayúsculas         | Especialidad("MECANICA")                    | Normalizado a minúsculas
ESP-005      | Normalizar espacios           | Especialidad("  electricidad  ")            | Espacios eliminados
ESP-006      | Rechazo especialidad inválida  | Intentar Especialidad("astronauta")         | Lanza ValueError
ESP-007      | Rechazo tipo no string        | Intentar Especialidad(123)                  | Lanza TypeError
ESP-008      | Todas válidas                 | Crear las 8 especialidades válidas          | Todas se crean exitosamente
ESP-009      | Igualdad                      | Especialidad("mecanica") == ...             | Son iguales
ESP-010      | Desigualdad                   | Especialidad("mecanica") != ...             | No son iguales
ESP-011      | Hasheable - en sets           | {Especialidad(...), Especialidad(...)}      | Set contiene 1 elemento
ESP-012      | Uso en diccionarios           | dict con Especialidad como clave            | Se pueden usar como claves
ESP-013      | Representación string         | repr(Especialidad("suspension"))            | Contiene "suspension"
"""
import pytest
from backend.value_objects.especialidad import Especialidad


class TestEspecialidad:
    """Pruebas para el value object Especialidad"""
    
    def test_especialidad_001_creacion_mecanica(self):
        """Crear especialidad Mecánica"""
        esp = Especialidad("mecanica")
        assert esp.nombre == "mecanica"
        assert esp.es_mecanica is True
    
    def test_especialidad_002_creacion_electricidad(self):
        """Crear especialidad Electricidad"""
        esp = Especialidad("electricidad")
        assert esp.nombre == "electricidad"
        assert esp.es_electricidad is True
    
    def test_especialidad_003_creacion_sistemas(self):
        """Crear especialidad Sistemas"""
        esp = Especialidad("sistemas")
        assert esp.nombre == "sistemas"
        assert esp.es_sistemas is True
    
    def test_especialidad_004_normalizacion_mayusculas(self):
        """Normalizar especialidad a minúsculas"""
        esp = Especialidad("MECANICA")
        assert esp.nombre == "mecanica"
    
    def test_especialidad_005_normalizacion_espacios(self):
        """Eliminar espacios en blanco"""
        esp = Especialidad("  electricidad  ")
        assert esp.nombre == "electricidad"
    
    def test_especialidad_006_rechazo_invalida(self):
        """Rechazar especialidad no válida"""
        with pytest.raises(ValueError, match="Especialidad inválida"):
            Especialidad("astronauta")
    
    def test_especialidad_007_rechazo_tipo_invalido(self):
        """Rechazar especialidad con tipo no string"""
        with pytest.raises(TypeError):
            Especialidad(123)
    
    def test_especialidad_008_todas_especialidades_validas(self):
        """Crear todas las especialidades válidas"""
        especiales_validas = [
            "mecanica", "electricidad", "suspension", "sistemas",
            "chapa", "pintura", "tapiceria", "transmision"
        ]
        for esp_nombre in especiales_validas:
            esp = Especialidad(esp_nombre)
            assert esp.nombre == esp_nombre
    
    def test_especialidad_009_igualdad(self):
        """Dos especialidades iguales son iguales"""
        e1 = Especialidad("mecanica")
        e2 = Especialidad("mecanica")
        assert e1 == e2
    
    def test_especialidad_010_desigualdad(self):
        """Especialidades distintas no son iguales"""
        e1 = Especialidad("mecanica")
        e2 = Especialidad("electricidad")
        assert e1 != e2
    
    def test_especialidad_011_hasheable(self):
        """Especialidad es hasheable"""
        e1 = Especialidad("mecanica")
        e2 = Especialidad("mecanica")
        esp_set = {e1, e2}
        assert len(esp_set) == 1
    
    def test_especialidad_012_puede_usarse_en_dict(self):
        """Usar especialidad como clave de diccionario"""
        e1 = Especialidad("electricidad")
        e2 = Especialidad("electricidad")
        empleados = {e1: ["Juan", "María"]}
        assert empleados[e2] == ["Juan", "María"]
    
    def test_especialidad_013_representacion_string(self):
        """Verificar representación en string"""
        esp = Especialidad("suspension")
        assert "suspension" in repr(esp)
