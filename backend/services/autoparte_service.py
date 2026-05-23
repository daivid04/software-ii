from sqlalchemy.orm import Session
from repositories.autoparte_repo import AutoparteRepository
from schemas.autoparte_schema import AutoparteCreate
from core.cache import cache



class AutoparteService:

    def __init__(self, db: Session):
        self.repo = AutoparteRepository(db)
    
    def registrar_nueva_autoparte(self, data: AutoparteCreate):
        """Registra una nueva autoparte en el sistema"""
        if self.repo.buscar_autoparte_por_nombre(data.nombre):
            raise ValueError("Ya existe una autoparte con ese nombre")
        autoparte = self.repo.registrar_autoparte(data)
        
        # Invalidar caché de productos (autopartes heredan de productos)
        cache.invalidate_pattern('productos')
        
        return autoparte
    
    def obtener_catalogo_completo(self):
        """Obtiene el catálogo completo de autopartes"""
        return self.repo.listar_catalogo_autopartes()
    
    def consultar_autoparte_disponible(self, id: int):
        """Consulta si una autoparte está disponible"""
        return self.repo.consultar_autoparte(id)
    
    def buscar_autoparte_por_nombre(self, nombre: str):
        """Busca una autoparte por nombre"""
        return self.repo.buscar_autoparte_por_nombre(nombre)
    
    def actualizar_informacion_autoparte(self, id: int, data: AutoparteCreate):
        """Actualiza la información de una autoparte"""
        autoparte = self.repo.consultar_autoparte(id)
        if not autoparte:
            raise ValueError("La autoparte no existe")
        
        result = self.repo.actualizar_autoparte(id, data)
        
        # Invalidar caché de productos
        cache.delete(f'producto_{id}')
        cache.invalidate_pattern('productos')
        
        return result
    
    def dar_de_baja_autoparte(self, id: int):
        """Da de baja una autoparte del sistema"""
        autoparte = self.repo.consultar_autoparte(id)
        if not autoparte:
            raise ValueError("La autoparte no existe")
        
        result = self.repo.dar_de_baja_autoparte(id)
        
        # Invalidar caché de productos
        cache.delete(f'producto_{id}')
        cache.invalidate_pattern('productos')
        
        return result
    
    def buscar_autopartes_por_modelo(self, modelo: str):
        """Busca autopartes por modelo de vehículo"""
        return self.repo.buscar_autopartes_por_modelo(modelo)
    
    def buscar_autopartes_por_anio(self, anio: int):
        """Busca autopartes compatibles con un año específico"""
        return self.repo.buscar_autopartes_por_anio(anio)