from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from src.producto.domain.producto_domain import ProductoDomain
from db.base import Base

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

    def to_domain(self) -> "ProductoDomain":
        return ProductoDomain(
            id=self.id,
            nombre=self.nombre,
            descripcion=self.descripcion,
            precio_compra=self.precio_compra,
            precio_venta=self.precio_venta,
            marca=self.marca,
            categoria=self.categoria,
            stock=self.stock,
            stock_minimo=self.stock_minimo,
            codigo_barras=self.codigo_barras,
            img=self.img,
            tipo=self.tipo
        )

    def from_domain(self, domain: "ProductoDomain"):
        self.nombre = domain.nombre
        self.descripcion = domain.descripcion
        self.precio_compra = domain.precio_compra
        self.precio_venta = domain.precio_venta
        self.marca = domain.marca
        self.categoria = domain.categoria
        self.stock = domain.stock
        self.stock_minimo = domain.stock_minimo
        self.codigo_barras = domain.codigo_barras
        self.img = domain.img
        self.tipo = domain.tipo