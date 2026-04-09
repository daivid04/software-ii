from sqlalchemy.orm import Session
from repositories.servicio_repo import ServicioRepository
from schemas.servicio_schema import ServicioCreate
from core.cache import cache

class ServicioService:

    def __init__(self, db: Session):
        self.repo = ServicioRepository(db)
    
    def create_servicio(self, data: ServicioCreate):
        if self.repo.get_by_name(data.nombre):
            raise ValueError("Ya existe un servicio con ese nombre")
        servicio_data = data
        servicio = self.repo.create(servicio_data)
        
        # Invalidar caché
        cache.invalidate_pattern('servicios')
        
        return servicio
    
    def list_servicios(self):
        # Intentar obtener del caché
        cached = cache.get('servicios_list')
        if cached is not None:
            return cached
        
        # Si no está en caché, obtener de la BD
        servicios = self.repo.get_all()
        
        # Guardar en caché por 5 minutos
        cache.set('servicios_list', servicios, ttl_seconds=300)
        
        return servicios
    
    def get_by_id(self, id: int):
        cache_key = f'servicio_{id}'
        cached = cache.get(cache_key)
        if cached is not None:
            return cached
        
        servicio = self.repo.get_by_id(id)
        
        if servicio:
            cache.set(cache_key, servicio, ttl_seconds=300)
        
        return servicio
    
    def get_by_name(self, nombre: str):
        return self.repo.get_by_name(nombre)
    
    def update_servicio(self, id: int, data: ServicioCreate):
        # Verificar si existe otro servicio con el mismo nombre
        existing = self.repo.get_by_name(data.nombre)
        if existing and existing.id != id:
            raise ValueError("Ya existe un servicio con ese nombre")
        
        servicio = self.repo.update(id, data)
        
        # Invalidar caché
        cache.delete(f'servicio_{id}')
        cache.invalidate_pattern('servicios')
        
        return servicio
    
    def delete_servicio(self, id: int):
        try:
            result = self.repo.delete(id)
            
            # Invalidar caché
            cache.delete(f'servicio_{id}')
            cache.invalidate_pattern('servicios')
            
            return result
        except ValueError as e:
            raise e