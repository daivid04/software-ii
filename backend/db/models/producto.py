from sqlalchemy import Column, Integer, String, Float
from db.base import Base
from sqlalchemy.orm import relationship
from db.models.value_objects import PrecioVO, InventarioVO

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False, unique=True)
    descripcion = Column(String, nullable=False, default="")
    precio_venta = Column(Float, nullable=False)
    precio_compra = Column(Float, nullable=False)
    marca = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    stock_minimo = Column(Integer, nullable=False, default=0)
    codigo_barras = Column(String, nullable=True, unique=True)
    img = Column(String, nullable=True)
    tipo = Column(String, nullable=False)

    ventas = relationship("VentaProducto", back_populates="producto")
    
    __mapper_args__ = {
        'polymorphic_identity': 'producto',
        'polymorphic_on': tipo
    }

    # --- MÉTODOS DE DOMINIO ---

    def actualizar_informacion_basica(self, nombre: str, descripcion: str, marca: str, categoria: str):
        if not nombre or not marca:
            raise ValueError("Nombre y marca son obligatorios")
        self.nombre = nombre
        self.descripcion = descripcion
        self.marca = marca
        self.categoria = categoria

    def establecer_precios(self, precio_compra: float, precio_venta: float):
        precio_vo = PrecioVO(compra=precio_compra, venta=precio_venta)
        self.precio_compra = precio_vo.compra
        self.precio_venta = precio_vo.venta

    def ajustar_inventario(self, stock_actual: int, stock_minimo: int):
        inventario_vo = InventarioVO(stock_actual=stock_actual, stock_minimo=stock_minimo)
        self.stock = inventario_vo.stock_actual
        self.stock_minimo = inventario_vo.stock_minimo