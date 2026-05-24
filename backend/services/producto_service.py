from sqlalchemy.orm import Session
from repositories.producto_repo import ProductoRepository
from schemas.producto_schema import ProductoCreate
from db.models.producto import Producto
from core.cache import cache


class ProductoService:

    def __init__(self, db: Session):
        self.repo = ProductoRepository(db)
    
    def registrar_nuevo_producto(self, data: ProductoCreate):
        """Registra un nuevo producto en el sistema"""
        if self.repo.buscar_producto_por_nombre(data.nombre):
            raise ValueError("Ya existe un producto con ese nombre")
        
        nuevo_producto = Producto(
            codigo_barras=data.codigo_barras,
            img=data.img,
            tipo="producto"
        )
        
        nuevo_producto.actualizar_informacion_basica(data.nombre, data.descripcion, data.marca, data.categoria)
        nuevo_producto.establecer_precios(data.precio_compra, data.precio_venta)
        nuevo_producto.ajustar_inventario(data.stock, data.stock_minimo)
        
        producto_guardado = self.repo.guardar(nuevo_producto)
        cache.invalidate_pattern('productos')
        return producto_guardado

    def obtener_catalogo_completo(self):
        """Obtiene el catálogo completo de productos"""
        # Intentar obtener del caché
        cached = cache.get('productos_list')
        if cached is not None:
            return cached
        
        # Si no está en caché, obtener de la BD
        productos = self.repo.listar_catalogo_productos()
        
        # Guardar en caché por 5 minutos
        cache.set('productos_list', productos, ttl_seconds=300)
        
        return productos
    
    def consultar_producto_disponible(self, id: int):
        """Consulta si un producto está disponible"""
        # Intentar obtener del caché
        cache_key = f'producto_{id}'
        cached = cache.get(cache_key)
        if cached is not None:
            return cached
        
        # Si no está en caché, obtener de la BD
        producto = self.repo.consultar_producto(id)
        
        # Guardar en caché
        if producto:
            cache.set(cache_key, producto, ttl_seconds=300)
        
        return producto
    
    def buscar_producto_por_nombre(self, nombre: str):
        """Busca un producto por nombre en el catálogo"""
        return self.repo.buscar_producto_por_nombre(nombre)
    
    def escanear_codigo_barras(self, codigo_barras: str):
        """Escanea un código de barras para obtener el producto"""
        return self.repo.escanear_codigo_barras(codigo_barras)
    
    def actualizar_stock_y_precios(self, id: int, data: ProductoCreate):
        """Actualiza el stock y precios del producto"""
        producto = self.repo.consultar_producto(id)
        if not producto: return None
        
        producto.actualizar_informacion_basica(data.nombre, data.descripcion, data.marca, data.categoria)
        producto.establecer_precios(data.precio_compra, data.precio_venta)
        producto.ajustar_inventario(data.stock, data.stock_minimo)
        
        if data.codigo_barras is not None: producto.codigo_barras = data.codigo_barras
        if data.img is not None: producto.img = data.img
            
        producto_actualizado = self.repo.actualizar_inventario_producto(producto)
        
        cache.delete(f'producto_{id}')
        cache.invalidate_pattern('productos')
        return producto_actualizado
    
    def dar_de_baja_producto(self, id: int):
        """Da de baja un producto del sistema"""
        try:
            result = self.repo.dar_de_baja_producto(id)
            
            # Invalidar caché
            cache.delete(f'producto_{id}')
            cache.invalidate_pattern('productos')
            
            return result
        except ValueError as e:
            raise e