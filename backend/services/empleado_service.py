from sqlalchemy.orm import Session
from repositories.empleado_repo import EmpleadoRepository
from schemas.empleado_schema import EmpleadoCreate
from db.models.empleado import Empleado
from core.cache import cache

class EmpleadoService:

    def __init__(self, db: Session):
        self.repo = EmpleadoRepository(db)
    
    def registrar_nuevo_empleado(self, data: EmpleadoCreate):
        """Registra un nuevo empleado en el sistema"""
        """Registra un nuevo empleado validando las reglas de dominio"""
        if self.repo.buscar_empleado_por_nombre(data.nombres):
            raise ValueError("Ya existe un empleado registrado con esos nombres")
        
        # 1. Instanciamos el agregado
        nuevo_empleado = Empleado()
        
        # 2. El agregado aplica el Lenguaje Ubicuo y se auto-valida
        nuevo_empleado.actualizar_informacion(data.nombres, data.apellidos, data.especialidad)
        nuevo_empleado.cambiar_estado(data.estado)
        
        # 3. Guardamos
        empleado_guardado = self.repo.guardar(nuevo_empleado)
        
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
        """El coordinador pasa los datos para que el agregado se modifique a sí mismo"""
        existing = self.repo.buscar_empleado_por_nombre(data.nombres)
        if existing and existing.id != id:
            raise ValueError("Ya existe otro empleado con esos nombres")

        empleado = self.repo.consultar_empleado(id)
        if not empleado:
            return None
            
        # DDD: El Agregado modifica su propio estado interno
        empleado.actualizar_informacion(data.nombres, data.apellidos, data.especialidad)
        empleado.cambiar_estado(data.estado)
        
        empleado_actualizado = self.repo.guardar(empleado)
        
        cache.delete(f'empleado_{id}')
        cache.invalidate_pattern('empleados')
        return empleado_actualizado
    
    def dar_de_baja_empleado(self, id: int):
        """Da de baja un empleado del sistema"""
        result = self.repo.dar_de_baja_empleado(id)
        cache.delete(f'empleado_{id}')
        cache.invalidate_pattern('empleados')
        return result