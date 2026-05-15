import re

class CodigoBarra:
    """Value Object para códigos de barras"""
    
    # Soporta EAN-13, EAN-8, UPC-A
    PATRONES_VALIDOS = [
        r'^\d{8}$',      # EAN-8
        r'^\d{12}$',     # UPC-A
        r'^\d{13}$',     # EAN-13
        r'^\d{14}$'      # GTIN-14
    ]
    
    def __init__(self, codigo: str):
        if not isinstance(codigo, str):
            raise TypeError("Código de barras debe ser una cadena")
        codigo = codigo.strip()
        if not any(re.match(patron, codigo) for patron in self.PATRONES_VALIDOS):
            raise ValueError(
                f"Código de barras inválido. Formatos válidos: EAN-8, UPC-A, EAN-13, GTIN-14"
            )
        if not self._validar_digito_verificador(codigo):
            raise ValueError("Dígito verificador inválido")
        self._codigo = codigo
    
    @staticmethod
    def _validar_digito_verificador(codigo: str) -> bool:
        """Valida el dígito verificador usando el algoritmo de módulo 10"""
        if len(codigo) < 8:
            return True  # No validar para códigos muy cortos
        
        digitos = [int(d) for d in codigo[:-1]]
        suma = 0
        
        for i, digito in enumerate(digitos):
            if (i % 2 == 0 and len(codigo) in [8, 13]) or (i % 2 == 1 and len(codigo) in [12, 14]):
                suma += digito * 3
            else:
                suma += digito
        
        digito_verificador = (10 - (suma % 10)) % 10
        return int(codigo[-1]) == digito_verificador
    
    @property
    def codigo(self) -> str:
        return self._codigo
    
    @property
    def tipo(self) -> str:
        longitud = len(self._codigo)
        return {
            8: "EAN-8",
            12: "UPC-A",
            13: "EAN-13",
            14: "GTIN-14"
        }.get(longitud, "Desconocido")
    
    def __eq__(self, otro):
        if not isinstance(otro, CodigoBarra):
            return False
        return self._codigo == otro._codigo
    
    def __hash__(self):
        return hash(self._codigo)
    
    def __repr__(self):
        return f"CodigoBarra({self._codigo})"
    
    def __str__(self):
        return self._codigo
