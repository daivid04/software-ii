"""
Pruebas de Value Object: Email

Tabla de Casos de Prueba:

ID           | Objetivo                      | Escenario (Precondición / Acción)           | Resultado Esperado
-----------  | ----------------------------- | ------------------------------------------- | --------------------------------
EML-001      | Creación válida               | Crear Email("usuario@example.com")          | Email se crea exitosamente
EML-002      | Normalizar mayúsculas         | Email("USUARIO@EXAMPLE.COM")                | Normalizado a minúsculas
EML-003      | Normalizar espacios           | Email("  usuario@example.com  ")            | Espacios eliminados
EML-004      | Rechazo sin arroba            | Intentar Email("usuarioexample.com")        | Lanza ValueError
EML-005      | Rechazo sin dominio           | Intentar Email("usuario@")                  | Lanza ValueError
EML-006      | Rechazo sin extensión TLD     | Intentar Email("usuario@example")           | Lanza ValueError
EML-007      | Rechazo múltiples @           | Intentar Email("usuario@domain@example.com")| Lanza ValueError
EML-008      | Rechazo caracteres inválidos  | Intentar Email("usuario!invalid@example.com")| Lanza ValueError
EML-009      | Rechazo tipo no string        | Intentar Email(123)                         | Lanza TypeError
EML-010      | Extracción usuario            | Email("john.doe@company.org").usuario       | Retorna "john.doe"
EML-011      | Extracción dominio            | Email("john@company.org").dominio           | Retorna "company.org"
EML-012      | Igualdad                      | Email(...) == Email(...)                    | Son iguales
EML-013      | Igualdad case-insensitive     | Email("Usuario@Example.com") == ...         | Son iguales (normalizado)
EML-014      | Desigualdad                   | Email("usuario1@...") != Email("usuario2@...") | No son iguales
EML-015      | Hasheable - en sets           | {Email(...), Email(...)}                    | Set contiene 1 elemento (deduplicado)
EML-016      | Representación string         | str(Email("test@example.com"))              | Retorna "test@example.com"
EML-017      | Formatos complejos válidos    | Crear Email con +tag, números, subdominio  | Todos se crean exitosamente
"""
import pytest
from backend.value_objects.email import Email


class TestEmail:
    """Pruebas para el value object Email"""
    
    def test_email_001_creacion_valida(self):
        """Crear Email con formato válido"""
        email = Email("usuario@example.com")
        assert email.direccion == "usuario@example.com"
    
    def test_email_002_normalizacion_mayusculas(self):
        """Normalizar Email a minúsculas"""
        email = Email("USUARIO@EXAMPLE.COM")
        assert email.direccion == "usuario@example.com"
    
    def test_email_003_normalizacion_espacios(self):
        """Eliminar espacios en blanco"""
        email = Email("  usuario@example.com  ")
        assert email.direccion == "usuario@example.com"
    
    def test_email_004_rechazo_sin_arroba(self):
        """Rechazar email sin @ (símbolo @)"""
        with pytest.raises(ValueError):
            Email("usuarioexample.com")
    
    def test_email_005_rechazo_sin_dominio(self):
        """Rechazar email sin dominio"""
        with pytest.raises(ValueError):
            Email("usuario@")
    
    def test_email_006_rechazo_sin_extension(self):
        """Rechazar email sin extensión TLD"""
        with pytest.raises(ValueError):
            Email("usuario@example")
    
    def test_email_007_rechazo_varios_arroba(self):
        """Rechazar email con múltiples @"""
        with pytest.raises(ValueError):
            Email("usuario@domain@example.com")
    
    def test_email_008_rechazo_caracteres_invalidos(self):
        """Rechazar email con caracteres inválidos"""
        with pytest.raises(ValueError):
            Email("usuario!invalid@example.com")
    
    def test_email_009_rechazo_tipo_invalido(self):
        """Rechazar email con tipo no string"""
        with pytest.raises(TypeError):
            Email(123)
    
    def test_email_010_extraccion_usuario(self):
        """Extraer usuario del email"""
        email = Email("john.doe@company.org")
        assert email.usuario == "john.doe"
    
    def test_email_011_extraccion_dominio(self):
        """Extraer dominio del email"""
        email = Email("john@company.org")
        assert email.dominio == "company.org"
    
    def test_email_012_igualdad(self):
        """Dos emails iguales son iguales"""
        e1 = Email("usuario@example.com")
        e2 = Email("usuario@example.com")
        assert e1 == e2
    
    def test_email_013_igualdad_case_insensitive(self):
        """Emails iguales ignoran mayúsculas"""
        e1 = Email("Usuario@Example.com")
        e2 = Email("usuario@example.com")
        assert e1 == e2
    
    def test_email_014_desigualdad(self):
        """Emails distintos no son iguales"""
        e1 = Email("usuario1@example.com")
        e2 = Email("usuario2@example.com")
        assert e1 != e2
    
    def test_email_015_hasheable(self):
        """Email es hasheable y puede usarse en sets/dicts"""
        e1 = Email("usuario@example.com")
        e2 = Email("usuario@example.com")
        email_set = {e1, e2}
        assert len(email_set) == 1
    
    def test_email_016_representacion_string(self):
        """Verificar representación en string"""
        email = Email("test@example.com")
        assert str(email) == "test@example.com"
    
    def test_email_017_formatos_validos_complejos(self):
        """Aceptar formatos complejos válidos"""
        emails_validos = [
            "user+tag@example.co.uk",
            "first.last@example.org",
            "user123@sub.domain.com",
            "a@example.museum"
        ]
        for email_str in emails_validos:
            email = Email(email_str)
            assert email.direccion == email_str.lower()
