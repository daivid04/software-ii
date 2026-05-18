from sqlalchemy.orm import Session
from repositories.orden_repo import OrdenRepository
from schemas.orden_schema import OrdenCreate
from fastapi import HTTPException
from core.cache import cache

class OrdenService:
    
    def __init__(self, db: Session):
        self.repo = OrdenRepository(db)

    def registrar_nueva_orden(self, data: OrdenCreate):
        servicios = getattr(data, "servicios", None)
        empleados = getattr(data, "empleados", None)

        servicios_list = [p.model_dump() if hasattr(p, 'model_dump') else p for p in servicios] if servicios else []
        empleados_list = [p.model_dump() if hasattr(p, 'model_dump') else p for p in empleados] if empleados else []

        # Si hay servicios o empleados asociados, crear con relaciones
        if servicios_list or empleados_list:
            try:
                orden = self.repo.registrar_orden_con_servicios(
                    data.garantia,
                    data.estadoPago,
                    data.precio,
                    data.fecha,
                    servicios_list,
                    empleados_list,
                )
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
        else:
            # Caso simple: solo la orden
            orden = self.repo.registrar_orden(data.garantia, data.estadoPago, data.precio, data.fecha)
        
        # Invalidar caché cuando se crea nueva orden
        cache.invalidate_pattern('ordenes')
        return orden

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
        ordenes = self.repo.consultar_ordenes_por_fecha(fecha)
        return ordenes

    def dar_de_baja_orden(self, id: int):
        result = self.repo.dar_de_baja_orden(id)
        
        # Invalidar caché cuando se da de baja
        cache.delete(f'orden_{id}')
        cache.invalidate_pattern('ordenes')
        
        return result