from sqlalchemy.orm import Session
from fastapi import HTTPException
from core.cache import cache
from src.ordenes.infrastructure.orden_schema import OrdenCreate
from src.ordenes.infrastructure.orden import Orden
from src.ordenes.infrastructure.orden_repo import OrdenRepository
from src.servicios.infrastructure.servicio_repo import ServicioRepository
from src.empleados.infrastructure.empleado_repo import EmpleadoRepository
from src.ordenes.infrastructure.orden_empleado import OrdenEmpleado
from src.ordenes.infrastructure.orden_servicio import OrdenServicio


class OrdenService:
    
    def __init__(self, db: Session):
        self.repo = OrdenRepository(db)
        self.servicio_repo = ServicioRepository(db)
        self.empleado_repo = EmpleadoRepository(db)

    def registrar_nueva_orden(self, data: OrdenCreate):
        nueva_orden_orm = Orden()
        domain = nueva_orden_orm.to_domain()
        
        try:
            domain.inicializar_datos_basicos(data.garantia, data.estadoPago, data.precio, data.fecha)
            
            # Asociar Servicios
            servicios = getattr(data, "servicios", []) or []
            for item in servicios:
                servicio_db = self.servicio_repo.consultar_servicio(item.servicio_id)
                if not servicio_db:
                    raise ValueError(f"El servicio con ID {item.servicio_id} no existe")
                
                domain.agregar_servicio(item.servicio_id, item.precio_servicio)
                
                detalle_servicio = OrdenServicio(servicio_id=item.servicio_id, precio_servicio=item.precio_servicio)
                nueva_orden_orm.servicios.append(detalle_servicio)
            
            # Asociar Empleados
            empleados = getattr(data, "empleados", []) or []
            for item in empleados:
                empleado_db = self.empleado_repo.consultar_empleado(item.empleado_id)
                if not empleado_db:
                    raise ValueError(f"El empleado con ID {item.empleado_id} no existe")
                
                # Le pasamos el estado puro al dominio
                domain.asignar_empleado(item.empleado_id, empleado_db.estado, empleado_db.nombres)
                
                detalle_empleado = OrdenEmpleado(empleado_id=item.empleado_id)
                nueva_orden_orm.empleados.append(detalle_empleado)
            
            nueva_orden_orm.from_domain(domain)
            orden_guardada = self.repo.guardar(nueva_orden_orm)
            
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