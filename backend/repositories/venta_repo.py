from datetime import datetime

from sqlalchemy import Date, cast
from sqlalchemy.orm import Session

from db.models import Venta
from db.models import VentaProducto
from db.models import Producto


class VentaRepository:
    """
    Repositorio para Venta
    
    Responsable de la persistencia del Aggregate Root Venta.
    """
    
    def __init__(self, db: Session):
        self.db = db

    def create(self, fecha: datetime):
        """Crea una venta simple sin productos."""
        venta = Venta(fecha=fecha)
        self.db.add(venta)
        self.db.commit()
        self.db.refresh(venta)
        return venta

    def create_with_products(self, fecha: datetime, productos: list[dict]):
        """
        Crea una venta con productos asociados.
        
        Valida que los productos existan y que haya stock suficiente.
        Usa los métodos del Aggregate Root para manipular la venta.
        """
        venta = Venta(fecha=fecha)
        self.db.add(venta)
        try:
            # flush to get venta.id without committing
            self.db.flush()

            for item in productos:
                pid = item.get("producto_id")
                cantidad = item.get("cantidad", 0)
                
                if not pid or cantidad <= 0:
                    raise ValueError("Producto o cantidad inválida")

                producto = self.db.query(Producto).filter(Producto.id == pid).with_for_update().first()
                if not producto:
                    raise ValueError(f"Producto con id {pid} no existe")
                if producto.stock < cantidad:
                    raise ValueError(f"Stock insuficiente para producto {pid}")
                
                # Crear relación venta-producto
                vp = VentaProducto(venta_id=venta.id, producto_id=pid, cantidad=cantidad)
                
                # Usar el método del Aggregate Root para agregar producto
                venta.agregar_producto(vp)

                # Actualizar stock
                producto.stock = producto.stock - cantidad

            # commit everything
            self.db.commit()
            # refresh to load relationships
            self.db.refresh(venta)
            return venta
        except Exception:
            self.db.rollback()
            raise

    def save(self, venta: Venta) -> Venta:
        """
        Guarda los cambios de una venta existente.
        
        Args:
            venta: La venta a guardar
            
        Returns:
            La venta actualizada
        """
        self.db.merge(venta)
        self.db.commit()
        self.db.refresh(venta)
        return venta

    def get_all(self):
        """Obtiene todas las ventas."""
        return self.db.query(Venta).all()

    def get_by_id(self, id: int):
        """Obtiene una venta por ID."""
        return self.db.query(Venta).filter(Venta.id == id).first()

    def delete(self, id: int):
        """Elimina una venta por ID."""
        venta = self.get_by_id(id)
        if venta:
            self.db.delete(venta)
            self.db.commit()
            return True
        return False

    def get_by_fecha(self, fecha: datetime):
        """Obtiene ventas por fecha."""
        return self.db.query(Venta).filter(
            cast(Venta.fecha, Date) == fecha.date()
        ).all()
