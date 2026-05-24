from sqlalchemy import Column, Integer, String, ForeignKey
from src.producto.infrastructure.producto import Producto
from src.autopartes.domain.autoparte_domain import AutoparteDomain

class Autoparte(Producto):
    __tablename__ = "autopartes"
    
    id = Column(Integer, ForeignKey('productos.id'), primary_key=True)
    modelo = Column(String, nullable=False)
    anio = Column(String(50), nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'autoparte',
    }

    def to_domain(self) -> AutoparteDomain:
        # 1. Obtenemos el objeto base (Producto)
        producto_base = super().to_domain()
        
        # 2. Retornamos la especialización (Autoparte)
        return AutoparteDomain(
            id=producto_base.id,
            nombre=producto_base.nombre,
            descripcion=producto_base.descripcion,
            precio_compra=producto_base.precio_compra,
            precio_venta=producto_base.precio_venta,
            marca=producto_base.marca,
            categoria=producto_base.categoria,
            stock=producto_base.stock,
            stock_minimo=producto_base.stock_minimo,
            codigo_barras=producto_base.codigo_barras,
            img=producto_base.img,
            tipo=producto_base.tipo,
            # Campos propios
            modelo=self.modelo,
            anio=self.anio
        )

    def from_domain(self, domain: AutoparteDomain):
        # 1. Actualizamos la parte base
        super().from_domain(domain)
        # 2. Actualizamos la parte específica
        self.modelo = domain.modelo
        self.anio = domain.anio