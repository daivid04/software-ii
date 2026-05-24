from sqlalchemy.orm import Session
from src.autopartes.infrastructure.autoparte_repo import AutoparteRepository
from schemas.autoparte_schema import AutoparteCreate
from src.autopartes.infrastructure.autoparte import Autoparte
from src.autopartes.domain.autoparte_domain import AutoparteDomain

from core.cache import cache



class AutoparteService:

    def __init__(self, db: Session):
        self.repo = AutoparteRepository(db)
    
    def registrar_nueva_autoparte(self, data: AutoparteCreate):
        if self.repo.buscar_autoparte_por_nombre(data.nombre):
            raise ValueError("Ya existe una autoparte con ese nombre")
        
        # 1. Crear el ORM (Infraestructura)
        nueva_autoparte = Autoparte(
            tipo="autoparte",
            codigo_barras=data.codigo_barras,
            img=data.img
        )
        
        # 2. Convertir a Dominio (Aquí es donde la lógica vive)
        domain = nueva_autoparte.to_domain()
        
        # 3. Aplicar lógica de negocio (Producto + Autoparte)
        domain.actualizar_informacion_basica(data.nombre, data.descripcion, data.marca, data.categoria)
        domain.establecer_precios(data.precio_compra, data.precio_venta)
        domain.ajustar_inventario(data.stock, data.stock_minimo)
        domain.asignar_compatibilidad(data.modelo, data.anio)
        
        # 4. Sincronizar de vuelta al ORM
        nueva_autoparte.from_domain(domain)

        producto_guardado = self.repo.guardar(nueva_autoparte)
        cache.invalidate_pattern('autopartes')
        return producto_guardado
    
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
        """
        CORRECCIÓN CRÍTICA: 
        Ya no llamamos métodos sobre 'autoparte' (ORM). 
        Ahora convertimos a dominio primero.
        """
        db_autoparte = self.repo.consultar_autoparte(id)
        if not db_autoparte:
            raise ValueError("La autoparte no existe")
        
        # 1. Convertimos a Dominio
        domain = db_autoparte.to_domain()
        
        # 2. Aplicamos lógica en el DOMINIO
        domain.actualizar_informacion_basica(data.nombre, data.descripcion, data.marca, data.categoria)
        domain.establecer_precios(data.precio_compra, data.precio_venta)
        domain.ajustar_inventario(data.stock, data.stock_minimo)
        domain.asignar_compatibilidad(data.modelo, data.anio)

        # 3. Sincronizamos los cambios del Dominio al ORM
        db_autoparte.from_domain(domain)
        
        # Campos extra que no están en el dominio puro pero sí en el ORM (opcional)
        if data.codigo_barras is not None: db_autoparte.codigo_barras = data.codigo_barras
        if data.img is not None: db_autoparte.img = data.img
        
        # 4. Guardamos
        result = self.repo.actualizar_autoparte(db_autoparte)
        
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