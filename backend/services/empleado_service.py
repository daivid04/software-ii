from sqlalchemy.orm import Session
from repositories.empleado_repo import EmpleadoRepository
from schemas.empleado_schema import EmpleadoCreate
from core.cache import cache

class EmpleadoService:

    def __init__(self, db: Session):
        self.repo = EmpleadoRepository(db)
    
    def registrar_nuevo_empleado(self, data: EmpleadoCreate):
        """Registra un nuevo empleado en el sistema"""
        if self.repo.buscar_empleado_por_nombre(data.nombres):
            raise ValueError("Ya existe un empleado con ese nombre")
        empleado = self.repo.registrar_empleado(data)
        
        # Invalidar caché cuando se crea nuevo empleado
        cache.invalidate_pattern('empleados')
        
        return empleado
    
    def obtener_catalogo_completo(self):
        """Obtiene el catálogo completo de empleados"""
        # Intentar obtener del caché
        cached = cache.get('empleados_list')
        if cached is not None:
            return cached
        
        # Si no está en caché, obtener de la BD
        empleados = self.repo.listar_catalogo_empleados()
        
        # Guardar en caché por 5 minutos
        cache.set('empleados_list', empleados, ttl_seconds=300)
        
        return empleados
    
    def consultar_empleado_activo(self, id: int):
        """Consulta un empleado activo por ID"""
        # Intentar obtener del caché
        cache_key = f'empleado_{id}'
        cached = cache.get(cache_key)
        if cached is not None:
            empleado = cached
        else:
            empleado = self.repo.consultar_empleado(id)
            if empleado:
                cache.set(cache_key, empleado, ttl_seconds=300)
        
        if empleado and empleado.estado == "activo":
            return empleado
        return None

    def actualizar_empleado(self, id: int, data: EmpleadoCreate):
        """Actualiza la información de un empleado"""
        empleado = self.repo.actualizar_empleado(id, data)
        
        # Invalidar caché cuando se actualiza
        cache.delete(f'empleado_{id}')
        cache.invalidate_pattern('empleados')
        
        return empleado
    
    def dar_de_baja_empleado(self, id: int):
        """Da de baja un empleado del sistema"""
        empleado = self.repo.dar_de_baja_empleado(id)
        
        # Invalidar caché cuando se da de baja
        cache.delete(f'empleado_{id}')
        cache.invalidate_pattern('empleados')
        
        return empleado