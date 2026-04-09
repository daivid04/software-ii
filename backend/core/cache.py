from datetime import datetime, timedelta
from typing import Optional, Any, Dict
import json

class SimpleCache:
    """
    Caché en memoria simple con TTL (Time To Live)
    """
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """
        Obtiene un valor del caché si existe y no ha expirado
        """
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        if datetime.now() > entry['expires_at']:
            # Expiró, eliminar
            del self._cache[key]
            return None
        
        return entry['value']
    
    def set(self, key: str, value: Any, ttl_seconds: int = 300):
        """
        Guarda un valor en el caché con un TTL (por defecto 5 minutos)
        """
        self._cache[key] = {
            'value': value,
            'expires_at': datetime.now() + timedelta(seconds=ttl_seconds)
        }
    
    def delete(self, key: str):
        """
        Elimina una entrada del caché
        """
        if key in self._cache:
            del self._cache[key]
    
    def clear(self):
        """
        Limpia todo el caché
        """
        self._cache.clear()
    
    def invalidate_pattern(self, pattern: str):
        """
        Invalida todas las claves que coincidan con un patrón
        Ejemplo: invalidate_pattern('productos') elimina todas las claves que contengan 'productos'
        """
        keys_to_delete = [key for key in self._cache.keys() if pattern in key]
        for key in keys_to_delete:
            del self._cache[key]

# Instancia global del caché
cache = SimpleCache()
