from sqlalchemy.orm import Session
from src.empleados.infrastructure.empleado_repo import EmpleadoRepository
from src.empleados.infrastructure.empleado_schema import EmpleadoCreate
from src.empleados.infrastructure.empleado import Empleado
from core.cache import cache

class EmpleadoService:

    def __init__(self, db: Session):
        self.repo = EmpleadoRepository(db)
    
    def registrar_nuevo_empleado(self, data: EmpleadoCreate):
        """Registra un nuevo empleado en el sistema"""
        if self.repo.buscar_empleado_por_nombre(data.nombres):
            raise ValueError("Ya existe un empleado registrado con esos nombres")
        
        # 1. ORM base y paso a Dominio
        nuevo_empleado_orm = Empleado()
        domain = nuevo_empleado_orm.to_domain()
        
        # 2. Lógica de negocio (Dominio)
        domain.actualizar_informacion(data.nombres, data.apellidos, data.especialidad)
        domain.cambiar_estado(data.estado)
        
        # 3. Sincronizar y guardar (Infraestructura)
        nuevo_empleado_orm.from_domain(domain)
        empleado_guardado = self.repo.guardar(nuevo_empleado_orm)
        
        cache.invalidate_pattern('empleados')
        return empleado_guardado
    
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
        empleado = cached if cached is not None else self.repo.consultar_empleado(id)
        
        if empleado and not cached:
            cache.set(cache_key, empleado, ttl_seconds=300)
            
        if empleado and empleado.estado == "activo":
            return empleado
        return None

    def actualizar_empleado(self, id: int, data: EmpleadoCreate):
        """Actualiza la información de un empleado"""
        existing = self.repo.buscar_empleado_por_nombre(data.nombres)
        if existing and existing.id != id:
            raise ValueError("Ya existe otro empleado con esos nombres")

        db_empleado = self.repo.consultar_empleado(id)
        if not db_empleado:
            return None
            
        # 1. Conversión a Dominio
        domain = db_empleado.to_domain()

        # 2. Lógica
        domain.actualizar_informacion(data.nombres, data.apellidos, data.especialidad)
        domain.cambiar_estado(data.estado)
        
        # 3. Sincronización a ORM
        db_empleado.from_domain(domain)
        empleado_actualizado = self.repo.guardar(db_empleado)
        
        cache.delete(f'empleado_{id}')
        cache.invalidate_pattern('empleados')
        return empleado_actualizado
    
    def dar_de_baja_empleado(self, id: int):
        """Da de baja un empleado del sistema"""
        result = self.repo.dar_de_baja_empleado(id)
        cache.delete(f'empleado_{id}')
        cache.invalidate_pattern('empleados')
        return result