from sqlalchemy.orm import Session
from repositories.autoparte_repo import AutoparteRepository
from schemas.autoparte_schema import AutoparteCreate
from db.models.autoparte import Autoparte
from core.cache import cache



class AutoparteService:

    def __init__(self, db: Session):
        self.repo = AutoparteRepository(db)
    
    def registrar_nueva_autoparte(self, data: AutoparteCreate):
        """Registra una nueva autoparte en el sistema"""
        if self.repo.buscar_autoparte_por_nombre(data.nombre):
            raise ValueError("Ya existe una autoparte con ese nombre")
        
        # 1. Instanciamos la entidad base
        nueva_autoparte = Autoparte(
            codigo_barras=data.codigo_barras,
            img=data.img,
            tipo="autoparte"
        )
        
        # 2. Invocamos comportamiento heredado de Producto (DDD)
        nueva_autoparte.actualizar_informacion_basica(data.nombre, data.descripcion, data.marca, data.categoria)
        nueva_autoparte.establecer_precios(data.precio_compra, data.precio_venta)
        nueva_autoparte.ajustar_inventario(data.stock, data.stock_minimo)
        
        # 3. Invocamos comportamiento específico de Autoparte (DDD)
        nueva_autoparte.asignar_compatibilidad(data.modelo, data.anio)
        
        # 4. Guardamos a través del repo
        autoparte_guardada = self.repo.guardar(nueva_autoparte)
        cache.invalidate_pattern('productos')
        return autoparte_guardada
    
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
        
        # Modificamos el estado a través del modelo rico
        autoparte.actualizar_informacion_basica(data.nombre, data.descripcion, data.marca, data.categoria)
        autoparte.establecer_precios(data.precio_compra, data.precio_venta)
        autoparte.ajustar_inventario(data.stock, data.stock_minimo)
        autoparte.asignar_compatibilidad(data.modelo, data.anio)

        if data.codigo_barras is not None: autoparte.codigo_barras = data.codigo_barras
        if data.img is not None: autoparte.img = data.img
        
        result = self.repo.actualizar_autoparte(autoparte)
        
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