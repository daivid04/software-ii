from sqlalchemy.orm import Session
from src.servicios.infrastructure.servicio_repo import ServicioRepository
from src.servicios.infrastructure.servicio_schema import ServicioCreate
from src.servicios.infrastructure.servicio import Servicio
from core.cache import cache

class ServicioService:

    def __init__(self, db: Session):
        self.repo = ServicioRepository(db)
    
    def registrar_nuevo_servicio(self, data: ServicioCreate):
        """Registra un nuevo servicio en el sistema"""
        """Registra un nuevo servicio usando DDD"""
        if self.repo.buscar_servicio_por_nombre(data.nombre):
            raise ValueError("Ya existe un servicio con ese nombre")
            
        # 1. Instanciamos ORM
        nuevo_servicio_orm = Servicio()
        
        # 2. Convertimos a Dominio
        domain = nuevo_servicio_orm.to_domain()
        
        # 3. Lógica
        domain.actualizar_informacion(data.nombre, data.descripcion)
        
        # 4. Sincronizamos ORM y Guardamos
        nuevo_servicio_orm.from_domain(domain)
        servicio_guardado = self.repo.guardar(nuevo_servicio_orm)
        
        cache.invalidate_pattern('servicios')
        return servicio_guardado
    
    def obtener_catalogo_completo(self):
        """Obtiene el catálogo completo de servicios"""
        # Intentar obtener del caché
        cached = cache.get('servicios_list')
        if cached is not None:
            return cached
        
        # Si no está en caché, obtener de la BD
        servicios = self.repo.listar_catalogo_servicios()
        
        # Guardar en caché por 5 minutos
        cache.set('servicios_list', servicios, ttl_seconds=300)
        
        return servicios
    
    def consultar_servicio_disponible(self, id: int):
        """Consulta si un servicio está disponible"""
        cache_key = f'servicio_{id}'
        cached = cache.get(cache_key)
        if cached is not None:
            return cached
        
        servicio = self.repo.consultar_servicio(id)
        
        if servicio:
            cache.set(cache_key, servicio, ttl_seconds=300)
        
        return servicio
    
    def buscar_servicio_por_nombre(self, nombre: str):
        """Busca un servicio por nombre"""
        return self.repo.buscar_servicio_por_nombre(nombre)
    
    def actualizar_informacion_servicio(self, id: int, data: ServicioCreate):
        """Actualiza la información de un servicio"""
        """Actualiza el servicio delegando al Agregado"""
        existing = self.repo.buscar_servicio_por_nombre(data.nombre)
        if existing and existing.id != id:
            raise ValueError("Ya existe otro servicio con ese nombre")
            
        db_servicio = self.repo.consultar_servicio(id)
        if not db_servicio:
            return None
            
        # 1. ORM a Dominio
        domain = db_servicio.to_domain()
        
        # 2. Lógica
        domain.actualizar_informacion(data.nombre, data.descripcion)
        
        # 3. Dominio a ORM
        db_servicio.from_domain(domain)
        
        # 4. Guardar
        servicio_actualizado = self.repo.guardar(db_servicio)
        
        cache.delete(f'servicio_{id}')
        cache.invalidate_pattern('servicios')
        return servicio_actualizado
    
    def dar_de_baja_servicio(self, id: int):
        result = self.repo.dar_de_baja_servicio(id)
        if result:
            cache.delete(f'servicio_{id}')
            cache.invalidate_pattern('servicios')
        return result