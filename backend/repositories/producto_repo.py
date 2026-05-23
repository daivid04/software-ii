from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.models import Producto
from schemas.producto_schema import ProductoCreate


class ProductoRepository:

    def __init__(self, db: Session):
        self.db = db
    
    def registrar_producto(self, producto_data: ProductoCreate):
        """Registra un nuevo producto en el catálogo"""
        producto = Producto(**producto_data.model_dump())
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def listar_catalogo_productos(self):
        """Lista todos los productos del catálogo"""
        return self.db.query(Producto).all()
    
    def consultar_producto(self, id: int):
        """Consulta un producto por su ID"""
        return self.db.query(Producto).filter(Producto.id == id).first()
    
    def buscar_producto_por_nombre(self, nombre: str):
        """Busca un producto por nombre"""
        return self.db.query(Producto).filter(Producto.nombre.ilike(nombre)).first()
    
    def escanear_codigo_barras(self, codigo_barras: str):
        """Escanea un código de barras y devuelve el producto"""
        return self.db.query(Producto).filter(Producto.codigo_barras == codigo_barras).first()

    def actualizar_inventario_producto(self, id: int, producto_data: ProductoCreate):
        """Actualiza el inventario del producto (precios, stock, etc.)"""
        producto = self.consultar_producto(id)
        if not producto:
            return None
        data = producto_data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(producto, key, value)
        self.db.commit()
        self.db.refresh(producto)
        return producto
    
    def dar_de_baja_producto(self, id: int):
        """Da de baja un producto del catálogo"""
        producto = self.consultar_producto(id)
        if producto:
            try:
                self.db.delete(producto)
                self.db.commit()
            except IntegrityError as e:
                self.db.rollback()
                raise ValueError(f"No se puede dar de baja el producto porque tiene ventas o referencias asociadas")
        return producto