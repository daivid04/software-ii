class FakeEmpleadoRepository:
    """Simula el repositorio de Empleados en memoria RAM sin tocar PostgreSQL"""
    
    def __init__(self, db=None):
        self.db_falsa = []
        self._id_counter = 1

    def guardar(self, empleado):
        # Simulamos el comportamiento de autoincremento de SQL
        if getattr(empleado, 'id', None) is None:
            empleado.id = self._id_counter
            self._id_counter += 1
            self.db_falsa.append(empleado)
        return empleado
    
    def listar_catalogo_empleados(self):
        return self.db_falsa
    
    def consultar_empleado(self, id: int):
        for emp in self.db_falsa:
            # Usamos getattr para evitar errores con objetos ORM simulados
            if getattr(emp, 'id', None) == id:
                return emp
        return None

    def buscar_empleado_por_nombre(self, nombres: str):
        for emp in self.db_falsa:
            if emp.nombres == nombres:
                return emp
        return None

    def dar_de_baja_empleado(self, id: int):
        empleado = self.consultar_empleado(id)
        if empleado:
            # Simulamos el borrado exitoso
            self.db_falsa.remove(empleado)
            return empleado
        return None
    
class FakeServicioRepository:
    def __init__(self, db=None):
        self.db_falsa = []

    def consultar_servicio(self, id: int):
        for serv in self.db_falsa:
            if getattr(serv, 'id', None) == id:
                return serv
        return None
    
class FakeOrdenRepository:
    def __init__(self, db=None):
        self.db_falsa = []
        self._id_counter = 1

    def guardar(self, orden):
        if getattr(orden, 'id', None) is None:
            orden.id = self._id_counter
            self._id_counter += 1
        self.db_falsa.append(orden)
        return orden
    
class FakeProductoRepository:
    def __init__(self, db=None):
        self.db_falsa = []
        self._id_counter = 1

    def guardar(self, producto):
        if getattr(producto, 'id', None) is None:
            producto.id = self._id_counter
            self._id_counter += 1
            self.db_falsa.append(producto)
        return producto

    def buscar_producto_por_nombre(self, nombre: str):
        for prod in self.db_falsa:
            if getattr(prod, 'nombre', None) == nombre:
                return prod
        return None

    def consultar_producto(self, id: int):
        for prod in self.db_falsa:
            if getattr(prod, 'id', None) == id:
                return prod
        return None

    def dar_de_baja_producto(self, id: int):
        producto = self.consultar_producto(id)
        if producto:
            self.db_falsa.remove(producto)
            return producto
        raise ValueError("Producto no encontrado")
    
class FakeAutoparteRepository:
    def __init__(self, db=None):
        self.db_falsa = []
        self._id_counter = 1

    def guardar(self, autoparte):
        if getattr(autoparte, 'id', None) is None:
            autoparte.id = self._id_counter
            self._id_counter += 1
            self.db_falsa.append(autoparte)
        return autoparte

    def listar_catalogo_autopartes(self):
        return self.db_falsa

    def consultar_autoparte(self, id: int):
        for auto in self.db_falsa:
            if getattr(auto, 'id', None) == id:
                return auto
        return None

    def buscar_autoparte_por_nombre(self, nombre: str):
        for auto in self.db_falsa:
            if getattr(auto, 'nombre', None) == nombre:
                return auto
        return None
        
    def actualizar_autoparte(self, autoparte):
        # En memoria, el objeto ya está actualizado por referencia,
        # pero simulamos el comportamiento de devolver el objeto
        return autoparte

    def dar_de_baja_autoparte(self, id: int):
        autoparte = self.consultar_autoparte(id)
        if autoparte:
            self.db_falsa.remove(autoparte)
            return autoparte
        return None
        
    def buscar_autopartes_por_modelo(self, modelo: str):
        return [auto for auto in self.db_falsa if getattr(auto, 'modelo', None) == modelo]
        
    def buscar_autopartes_por_anio(self, anio: str):
        return [auto for auto in self.db_falsa if str(anio) in getattr(auto, 'anio', "")]
    
class FakeVentaRepository:
    def __init__(self, db=None):
        self.db_falsa = []
        self._id_counter = 1

    def guardar(self, venta):
        if getattr(venta, 'id', None) is None:
            venta.id = self._id_counter
            self._id_counter += 1
            self.db_falsa.append(venta)
        return venta

    def listar_registro_ventas(self):
        return self.db_falsa

    def consultar_venta(self, id: int):
        for venta in self.db_falsa:
            if getattr(venta, 'id', None) == id:
                return venta
        return None

    def consultar_ventas_por_fecha(self, fecha):
        # Simplificación para el test en memoria
        return [v for v in self.db_falsa if getattr(v, 'fecha', None) == fecha]

    def dar_de_baja_venta(self, id: int):
        venta = self.consultar_venta(id)
        if venta:
            self.db_falsa.remove(venta)
            return venta
        return None
    
class FakeServicioRepository:
    def __init__(self, db=None):
        self.db_falsa = []
        self._id_counter = 1

    def guardar(self, servicio):
        if getattr(servicio, 'id', None) is None:
            servicio.id = self._id_counter
            self._id_counter += 1
            self.db_falsa.append(servicio)
        return servicio

    def listar_catalogo_servicios(self):
        return self.db_falsa

    def consultar_servicio(self, id: int):
        for serv in self.db_falsa:
            if getattr(serv, 'id', None) == id:
                return serv
        return None

    def buscar_servicio_por_nombre(self, nombre: str):
        for serv in self.db_falsa:
            if getattr(serv, 'nombre', None) == nombre:
                return serv
        return None

    def dar_de_baja_servicio(self, id: int):
        servicio = self.consultar_servicio(id)
        if servicio:
            self.db_falsa.remove(servicio)
            return servicio
        return None