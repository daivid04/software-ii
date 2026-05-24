from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.producto.infrastructure.producto import Producto


class ProductoRepository:

    def __init__(self, db: Session):
        self.db = db

    def guardar(self, producto: Producto):
        """Persiste los cambios del Agregado en la base de datos"""
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