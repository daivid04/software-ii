from sqlalchemy.orm import Session
from repositories.autoparte_repo import AutoparteRepository
from schemas.autoparte_schema import AutoparteCreate
from core.cache import cache



class AutoparteService:

    def __init__(self, db: Session):
        self.repo = AutoparteRepository(db)
    
    def create_autoparte(self, data: AutoparteCreate):
        if self.repo.get_by_name(data.nombre):
            raise ValueError("Ya existe una autoparte con ese nombre")
        autoparte_data = data
        autoparte = self.repo.create(autoparte_data)
        
        # Invalidar caché de productos (autopartes heredan de productos)
        cache.invalidate_pattern('productos')
        
        return autoparte
    
    def list_autopartes(self):
        return self.repo.get_all()
    
    def get_by_id(self, id: int):
        return self.repo.get_by_id(id)
    
    def get_by_name(self, nombre: str):
        return self.repo.get_by_name(nombre)
    
    def update_autoparte(self, id: int, data: AutoparteCreate):
        autoparte = self.repo.get_by_id(id)
        if not autoparte:
            raise ValueError("La autoparte no existe")
        
        result = self.repo.update(id, data)
        
        # Invalidar caché de productos
        cache.delete(f'producto_{id}')
        cache.invalidate_pattern('productos')
        
        return result
    
    def delete_autoparte(self, id: int):
        autoparte = self.repo.get_by_id(id)
        if not autoparte:
            raise ValueError("La autoparte no existe")
        
        result = self.repo.delete(id)
        
        # Invalidar caché de productos
        cache.delete(f'producto_{id}')
        cache.invalidate_pattern('productos')
        
        return result
    
    def get_by_modelo(self, modelo: str):
        return self.repo.get_by_modelo(modelo)
    
    def get_by_anio(self, anio: int):
        """Busca autopartes compatibles con un año específico"""
        return self.repo.get_by_anio(anio)