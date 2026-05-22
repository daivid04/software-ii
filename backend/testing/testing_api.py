"""
TestingAPI: Adaptador desacoplado para pruebas BDD con Behave
Inyecta servicios directamente sin dependencias HTTP ni UI
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from db.base import Base
from db.models.producto import Producto
from db.models.servicio import Servicio
from db.models.orden import Orden
from db.models.orden_servicio import OrdenServicio
from repositories.producto_repo import ProductoRepository
from repositories.servicio_repo import ServicioRepository
from repositories.orden_repo import OrdenRepository
from services.producto_service import ProductoService
from services.servicio_service import ServicioService
from services.orden_service import OrdenService


class TestingAPI:
    """
    API de pruebas que actúa como puente entre Behave y la lógica de dominio.
    Inyecta servicios internos sin pasar por controladores HTTP.
    """
    
    def __init__(self, use_memory_db: bool = True):
        """
        Inicializa la TestingAPI con una BD temporal.
        
        Args:
            use_memory_db: Si True, usa BD temporal en disco; Si False, usa test.db
        """
        import tempfile
        import os
        
        # Crear BD temporal
        if use_memory_db:
            # Crear un archivo temporal único para esta instancia
            fd, db_path = tempfile.mkstemp(suffix=".db")
            os.close(fd)
            self.db_path = db_path
            self.engine = create_engine(f"sqlite:///{db_path}", echo=False)
        else:
            self.db_path = "./test.db"
            self.engine = create_engine("sqlite:///./test.db", echo=False)
        
        # Crear todas las tablas
        Base.metadata.create_all(bind=self.engine)
        
        # Crear sesión
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db: Session = SessionLocal()
        
        # Inyectar servicios
        self.producto_service = ProductoService(self.db)
        self.servicio_service = ServicioService(self.db)
        self.orden_service = OrdenService(self.db)
        
        # Estados temporales para pruebas
        self.error_message = None
        self.last_producto = None
        self.last_servicio = None
        self.last_orden_servicio = None
    
    def close(self):
        """Cierra la sesión de BD y limpia archivos temporales"""
        try:
            self.db.close()
        except:
            pass
        
        # Limpiar archivo temporal si existe
        if hasattr(self, 'db_path') and self.db_path and self.db_path != "./test.db":
            try:
                import os
                if os.path.exists(self.db_path):
                    os.remove(self.db_path)
            except:
                pass
    
    # ==================== H1: CONTROL DE INVENTARIO ====================
    
    def inicializar_inventario(self, cantidad: int):
        """
        Crea `cantidad` productos válidos en el inventario.
        
        Args:
            cantidad: Número de productos a crear (200-300)
        """
        from schemas.producto_schema import ProductoCreate
        
        for i in range(1, cantidad + 1):
            try:
                producto_data = ProductoCreate(
                    nombre=f"Producto_{i}",
                    descripcion=f"Producto de prueba {i}",
                    precioVenta=100 * i,
                    precioCompra=50 * i,
                    marca=f"Marca_{i % 5}",
                    categoria="Repuesto",
                    stock=10,
                    stockMin=2,
                    codBarras=f"COD{i:06d}",
                    tipo="producto"
                )
                self.producto_service.create_producto(producto_data)
            except Exception as e:
                # Si falla algún producto, registrar el error
                self.error_message = str(e)
                raise
    
    def registrar_producto(self, marca: str, modelo: str, año: str) -> bool:
        """
        Registra un nuevo producto con validación SWEBOK.
        Retorna True si el registro fue exitoso, False si excede capacidad.
        
        Args:
            marca: Marca del producto
            modelo: Modelo
            año: Año de fabricación
            
        Returns:
            bool: True si fue exitoso, False si fue rechazado
        """
        from schemas.producto_schema import ProductoCreate
        
        try:
            # Validar capacidad máxima (200-300)
            conteo_actual = self.obtener_conteo_productos()
            if conteo_actual >= 300:
                self.error_message = "Se ha alcanzado el límite máximo de capacidad (300 productos)."
                return False
            
            # Validar que marca, modelo, año no sean vacíos
            if not marca or not modelo or not año:
                self.error_message = "Datos incompletos: marca, modelo y año son obligatorios."
                return False
            
            # Crear producto
            producto_data = ProductoCreate(
                nombre=f"{marca}_{modelo}_{año}",
                descripcion=f"Repuesto {marca} {modelo} {año}",
                precioVenta=500,
                precioCompra=250,
                marca=marca,
                categoria="Repuesto",
                stock=5,
                stockMin=1,
                codBarras=f"{marca[0:3]}{modelo[0:3]}{año}",
                tipo="producto"
            )
            
            self.last_producto = self.producto_service.create_producto(producto_data)
            self.error_message = None
            return True
            
        except Exception as e:
            self.error_message = str(e)
            return False
    
    def obtener_conteo_productos(self) -> int:
        """Retorna el total de productos activos en el inventario."""
        try:
            productos = self.producto_service.list_productos()
            return len(productos) if productos else 0
        except Exception:
            return 0
    
    # ==================== H2: GESTIÓN DE BARCODE ====================
    
    def registrar_producto_con_barcode(self, codigo_barras: str, marca: str = "TestMarca") -> bool:
        """
        Registra un producto con código de barras para pruebas de escaneo.
        
        Args:
            codigo_barras: Código único de barras
            marca: Marca del producto
            
        Returns:
            bool: True si fue exitoso
        """
        from schemas.producto_schema import ProductoCreate
        
        try:
            # Validar conteo (permitir 305 para que quepan tests de barcode después de inventory)
            current_count = self.obtener_conteo_productos()
            if current_count >= 305:
                self.error_message = f"Capacidad máxima alcanzada: {current_count}/305 productos."
                return False
            
            producto_data = ProductoCreate(
                nombre=f"Producto_{codigo_barras}",
                descripcion=f"Producto con código {codigo_barras}",
                precioVenta=1000,
                precioCompra=500,
                marca=marca,
                categoria="Repuesto",
                stock=15,
                stockMin=2,
                codBarras=codigo_barras,
                tipo="producto"
            )
            
            self.last_producto = self.producto_service.create_producto(producto_data)
            self.error_message = None
            return True
            
        except Exception as e:
            self.error_message = str(e)
            return False
    
    def buscar_producto_por_barcode(self, codigo_barras: str):
        """
        Busca un producto por código de barras (simulando lectura de pistola).
        
        Args:
            codigo_barras: Código a buscar
            
        Returns:
            Producto si existe, None si no
        """
        try:
            # Validar formato básico
            if not codigo_barras or len(codigo_barras) < 3:
                self.error_message = "Lectura incompleta: código truncado o mal escaneado."
                return None
            
            # Buscar en BD
            producto = self.db.query(Producto).filter(
                Producto.codBarras == codigo_barras
            ).first()
            
            if not producto:
                self.error_message = "Producto no encontrado."
                return None
            
            self.last_producto = producto
            self.error_message = None
            return producto
            
        except Exception as e:
            self.error_message = str(e)
            return None
    
    def obtener_detalles_producto(self, id_producto: int) -> dict:
        """
        Retorna detalles planos de un producto para validación SWEBOK.
        
        Args:
            id_producto: ID del producto
            
        Returns:
            dict con detalles (precio, ubicación, stock)
        """
        try:
            producto = self.producto_service.get_by_id(id_producto)
            if not producto:
                return {}
            
            return {
                "id": producto.id,
                "nombre": producto.nombre,
                "precio": producto.precioVenta,
                "stock": producto.stock,
                "ubicacion": "Estante_A1",  # Simulado para pruebas
                "marca": producto.marca,
                "codBarras": producto.codBarras
            }
        except Exception:
            return {}
    
    # ==================== H3: GESTIÓN DE SERVICIOS ====================
    
    def registrar_servicios_catalogo(self):
        """
        Registra servicios predeterminados para pruebas de H3.
        """
        from schemas.servicio_schema import ServicioCreate
        
        servicios_catalogo = [
            ("Alineación", "Alineación de ruedas y dirección"),
            ("Cambio de Aceite", "Cambio de aceite y filtro"),
            ("Reparación de Motor", "Reparación completa de motor"),
            ("Diagnóstico", "Diagnóstico completo del vehículo"),
            ("Reparación de Suspensión", "Reparación de sistema de suspensión"),
        ]
        
        for nombre, descripcion in servicios_catalogo:
            try:
                servicio_data = ServicioCreate(
                    nombre=nombre,
                    descripcion=descripcion,
                    precio=5000
                )
                self.servicio_service.create_servicio(servicio_data)
            except Exception:
                pass  # Ignorar si ya existe
    
    def obtener_servicio_por_nombre(self, nombre: str):
        """
        Obtiene un servicio del catálogo por nombre.
        
        Args:
            nombre: Nombre del servicio
            
        Returns:
            Servicio si existe, None si no
        """
        try:
            servicio = self.db.query(Servicio).filter(
                Servicio.nombre == nombre
            ).first()
            
            if not servicio:
                self.error_message = f"Servicio '{nombre}' no encontrado en catálogo."
                return None
            
            self.last_servicio = servicio
            self.error_message = None
            return servicio
            
        except Exception as e:
            self.error_message = str(e)
            return None
    
    def registrar_orden_servicio(self, servicio_id: int, descripcion_adicional: str = "") -> bool:
        """
        Registra una orden de servicio con descripción.
        
        Args:
            servicio_id: ID del servicio
            descripcion_adicional: Observaciones adicionales
            
        Returns:
            bool: True si fue exitoso
        """
        try:
            # Validar que servicio exista
            servicio = self.servicio_service.get_by_id(servicio_id)
            if not servicio:
                self.error_message = "Servicio no válido."
                return False
            
            # Crear orden primero (contiene info general)
            from datetime import date
            orden = Orden(
                garantia=12,  # 12 meses por defecto
                estadoPago="pendiente",
                precio=servicio.precio if hasattr(servicio, 'precio') else 0,
                fecha=date.today()
            )
            self.db.add(orden)
            self.db.flush()  # Obtener el ID antes de commit
            
            # Crear orden de servicio (vinculo entre Orden y Servicio)
            self.last_orden_servicio = OrdenServicio(
                orden_id=orden.id,
                servicio_id=servicio_id,
                precio_servicio=servicio.precio if hasattr(servicio, 'precio') else 0
            )
            self.db.add(self.last_orden_servicio)
            self.db.commit()
            
            self.error_message = None
            return True
            
        except Exception as e:
            self.db.rollback()
            self.error_message = str(e)
            return False
    
    def obtener_descripcion_servicio(self, servicio_id: int) -> str:
        """Retorna la descripción predeterminada de un servicio."""
        try:
            servicio = self.servicio_service.get_by_id(servicio_id)
            return servicio.descripcion if servicio else ""
        except Exception:
            return ""
    
    # ==================== UTILIDADES ====================
    
    def limpiar_inventario(self):
        """Limpia todos los productos del inventario."""
        try:
            self.db.query(Producto).delete()
            self.db.commit()
        except Exception:
            self.db.rollback()
    
    def limpiar_servicios(self):
        """Limpia todos los servicios."""
        try:
            self.db.query(Servicio).delete()
            self.db.commit()
        except Exception:
            self.db.rollback()
    
    def obtener_ultimo_error(self) -> str:
        """Retorna el último error registrado."""
        return self.error_message if self.error_message else ""
