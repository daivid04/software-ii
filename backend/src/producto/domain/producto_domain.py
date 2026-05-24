from dataclasses import dataclass
from src.shared.domain.value_objects import PrecioVO, InventarioVO

@dataclass
class ProductoDomain:
    """Clase pura de dominio. Sin SQLAlchemy, sin Base, solo lógica."""
    id: int | None
    nombre: str
    descripcion: str
    marca: str
    categoria: str
    precio_compra: float
    precio_venta: float
    stock: int
    stock_minimo: int
    codigo_barras: str | None
    img: str | None
    tipo: str

    def actualizar_informacion_basica(self, nombre: str, descripcion: str, marca: str, categoria: str):
        if not nombre or not marca:
            raise ValueError("Nombre y marca son obligatorios")
        self.nombre = nombre
        self.descripcion = descripcion
        self.marca = marca
        self.categoria = categoria

    def establecer_precios(self, compra: float, venta: float):
        vo = PrecioVO(compra=compra, venta=venta)
        self.precio_compra = vo.compra
        self.precio_venta = vo.venta

    def ajustar_inventario(self, actual: int, minimo: int):
        vo = InventarioVO(stock_actual=actual, stock_minimo=minimo)
        self.stock = vo.stock_actual
        self.stock_minimo = vo.stock_minimo

    def registrar_despacho(self, cantidad: int):
        if cantidad <= 0:
            raise ValueError("La cantidad a despachar debe ser mayor a 0")
            
        if self.stock < cantidad:
            raise ValueError(
                f"Stock insuficiente para '{self.nombre}'. "
                f"Stock actual: {self.stock}, Solicitado: {cantidad}"
            )
            
        # Si pasa las validaciones, descontamos el stock
        self.stock -= cantidad