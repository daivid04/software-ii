from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.ventas.infrastructure.venta_repo import VentaRepository
from src.producto.infrastructure.producto_repo import ProductoRepository
from src.ventas.infrastructure.venta import Venta
from db.models.venta_producto import VentaProducto
from core.cache import cache
from src.ventas.domain.venta_domain import VentaDomain


class VentaService:
    
    def __init__(self, db: Session):
        self.repo = VentaRepository(db)
        self.producto_repo = ProductoRepository(db)

    def registrar_nueva_venta(self, data):
        """Registra una nueva venta usando el Diseño Táctico (DDD)"""
        # 1. Creamos ORM vacío y convertimos a Dominio para usar su lógica
        nueva_venta_orm = Venta()
        domain = nueva_venta_orm.to_domain()
        
        # 2. Lógica de Dominio
        domain.inicializar_fecha(data.fecha)
        
        try:
            productos = getattr(data, "productos", None)
            if productos:
                for item in productos:
                    # 1. Obtenemos el ORM
                    producto_orm = self.producto_repo.consultar_producto(item.producto_id)
                    if not producto_orm:
                        raise ValueError(f"El producto con ID {item.producto_id} no existe")
                    
                    # 2. CONVERSIÓN: Pasamos el ORM a Dominio
                    producto_domain = producto_orm.to_domain()
                    
                    # 3. LÓGICA: Ahora sí podemos llamar al método de dominio
                    producto_domain.registrar_despacho(item.cantidad)
                    
                    # 4. SINCRONIZACIÓN: Actualizamos el ORM con los cambios del dominio
                    # (Esto actualiza el 'stock' en la instancia que SQLAlchemy guardará)
                    producto_orm.from_domain(producto_domain)
                    
                    # 5. Lógica de venta (la agregamos al dominio de venta)
                    domain.agregar_detalle(item.producto_id, item.cantidad)
                    
                    # 6. Creamos el detalle ORM para la venta (usando el ID del producto_orm)
                    detalle = VentaProducto(producto_id=producto_orm.id, cantidad=item.cantidad)
                    nueva_venta_orm.productos.append(detalle)
                    
                    # 7. Importante: Guardar el producto actualizado (o dejar que el servicio de producto lo haga)
                    # Dependiendo de tu repo, podrías necesitar un método para actualizar el producto
                    self.producto_repo.guardar(producto_orm)
            # 3. Sincronizar ORM de la venta
            nueva_venta_orm.from_domain(domain)
            cache.invalidate_pattern('productos') 
            cache.invalidate_pattern('autopartes')
            
            # --- AQUÍ ESTABA EL PROBLEMA ---
            # Este return debe estar fuera del 'if' y dentro del 'try'
            venta_guardada = self.repo.guardar(nueva_venta_orm)
            return venta_guardada
        except ValueError as e:
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
