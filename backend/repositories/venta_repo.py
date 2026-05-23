from datetime import datetime

from sqlalchemy import Date, cast
from sqlalchemy.orm import Session

from db.models import Venta
from db.models import VentaProducto
from db.models import Producto



class VentaRepository:
    def __init__(self, db: Session):
        self.db = db

    def registrar_venta(self, fecha: datetime):
        """Registra una nueva venta simple sin productos"""
        # Backwards-compatible create (no products)
        venta = Venta(fecha=fecha)
        self.db.add(venta)
        self.db.commit()
        self.db.refresh(venta)
        return venta

    def registrar_venta_con_productos(self, fecha: datetime, productos: list[dict]):
        """Registra una venta con múltiples productos y actualiza inventario"""
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
                    raise ValueError(f"Stock insuficiente.")
                
                # create relation venta-producto
                vp = VentaProducto(venta_id=venta.id, producto_id=pid, cantidad=cantidad)
                self.db.add(vp)

                # update stock
                producto.stock = producto.stock - cantidad

            # commit everything
            self.db.commit()
            # refresh to load relationships
            self.db.refresh(venta)
            return venta
        except Exception:
            self.db.rollback()
            raise

    def listar_registro_ventas(self):
        """Lista todas las ventas registradas"""
        return self.db.query(Venta).all()

    def consultar_venta(self, id: int):
        """Consulta una venta por su ID"""
        return self.db.query(Venta).filter(Venta.id == id).first()

    def dar_de_baja_venta(self, id: int):
        """Da de baja una venta del sistema"""
        venta = self.consultar_venta(id)
        if venta:
            self.db.delete(venta)
            self.db.commit()
            return True
        return False

    def consultar_ventas_por_fecha(self, fecha: datetime):
        """Consulta ventas por fecha específica"""
        return self.db.query(Venta).filter(
            cast(Venta.fecha, Date) == fecha.date()
        ).all()
