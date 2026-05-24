from sqlalchemy.orm import Session
from fastapi import HTTPException
from core.cache import cache
from schemas.orden_schema import OrdenCreate
from db.models.orden import Orden
from repositories.orden_repo import OrdenRepository
from repositories.servicio_repo import ServicioRepository
from repositories.empleado_repo import EmpleadoRepository
from db.models import OrdenServicio, OrdenEmpleado


class OrdenService:
    
    def __init__(self, db: Session):
        self.repo = OrdenRepository(db)
        self.servicio_repo = ServicioRepository(db)
        self.empleado_repo = EmpleadoRepository(db)

    def registrar_nueva_orden(self, data: OrdenCreate):
        """Coordina la creación de una orden utilizando el modelo de dominio rico"""
        nueva_orden = Orden()
        
        try:
            # 1. Validamos e inicializamos campos básicos
            nueva_orden.inicializar_datos_basicos(data.garantia, data.estadoPago, data.precio, data.fecha)
            
            # 2. El Agregado valida y asocia los Servicios
            servicios = getattr(data, "servicios", []) or []
            for item in servicios:
                servicio_db = self.servicio_repo.consultar_servicio(item.servicio_id)
                if not servicio_db:
                    raise ValueError(f"El servicio con ID {item.servicio_id} no existe")
                nueva_orden.agregar_servicio(servicio_db, item.precio_servicio, OrdenServicio)
            
            # 3. El Agregado valida y asocia a los Empleados
            empleados = getattr(data, "empleados", []) or []
            for item in empleados:
                empleado_db = self.empleado_repo.consultar_empleado(item.empleado_id)
                if not empleado_db:
                    raise ValueError(f"El empleado con ID {item.empleado_id} no existe")
                nueva_orden.asignar_empleado(empleado_db, OrdenEmpleado)
            
            # 4. El Repositorio guarda todo el árbol en una sola transacción
            orden_guardada = self.repo.guardar(nueva_orden)
            
            cache.invalidate_pattern('ordenes')
            return orden_guardada
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def obtener_catalogo_completo(self):
        # Intentar obtener del caché
        cached = cache.get('ordenes_list')
        if cached is not None:
            return cached
        
        # Si no está en caché, obtener de la BD
        ordenes = self.repo.listar_catalogo_ordenes()
        
        # Guardar en caché por 5 minutos
        cache.set('ordenes_list', ordenes, ttl_seconds=300)
        
        return ordenes

    def consultar_orden(self, id: int):
        # Intentar obtener del caché
        cache_key = f'orden_{id}'
        cached = cache.get(cache_key)
        if cached is not None:
            return cached
        
        # Si no está en caché, obtener de la BD
        orden = self.repo.consultar_orden(id)
        
        # Guardar en caché
        if orden:
            cache.set(cache_key, orden, ttl_seconds=300)
        
        return orden

    def consultar_ordenes_por_fecha(self, fecha):
        return self.repo.consultar_ordenes_por_fecha(fecha)

    def dar_de_baja_orden(self, id: int):
        result = self.repo.dar_de_baja_orden(id)
        if result:
            cache.delete(f'orden_{id}')
            cache.invalidate_pattern('ordenes')
        return result