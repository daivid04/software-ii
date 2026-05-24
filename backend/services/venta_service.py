from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session

from repositories.venta_repo import VentaRepository
from repositories.producto_repo import ProductoRepository
from schemas.venta_schema import VentaCreate
from db.models.venta import Venta
from db.models.venta_producto import VentaProducto


class VentaService:
    
    def __init__(self, db: Session):
        self.repo = VentaRepository(db)
        self.producto_repo = ProductoRepository(db)

    def registrar_nueva_venta(self, data: VentaCreate):
        """Registra una nueva venta usando el Diseño Táctico (DDD)"""
        nueva_venta = Venta()
        
        try:
            # 1. El modelo de Dominio valida la fecha
            nueva_venta.inicializar_fecha(data.fecha)
            
            productos = getattr(data, "productos", None)
            if productos:
                for item in productos:
                    # Buscamos el producto
                    producto = self.producto_repo.consultar_producto(item.producto_id)
                    if not producto:
                        raise ValueError(f"El producto con ID {item.producto_id} no existe")
                    
                    # 2. La Venta ejecuta su lógica de dominio (valida cantidad y actualiza el stock del producto)
                    nueva_venta.agregar_detalle(producto, item.cantidad, VentaProducto)
            
            # 3. El Repositorio guarda el Agregado en la BD
            return self.repo.guardar(nueva_venta)
            
        except ValueError as e:
            # Atrapamos errores de los Value Objects o reglas de negocio (Cantidades negativas, fechas erróneas, stock insuficiente)
            raise HTTPException(status_code=400, detail=str(e))

    def obtener_registro_completo_ventas(self):
        """Obtiene el registro completo de todas las ventas"""
        return self.repo.listar_registro_ventas()

    def consultar_venta(self, id: int):
        """Consulta una venta por su ID"""
        return self.repo.consultar_venta(id)

    def consultar_ventas_por_fecha(self, fecha: datetime):
        """Consulta ventas por una fecha específica"""
        return self.repo.consultar_ventas_por_fecha(fecha)

    def dar_de_baja_venta(self, id: int):
        """Da de baja una venta del sistema"""
        return self.repo.dar_de_baja_venta(id)
