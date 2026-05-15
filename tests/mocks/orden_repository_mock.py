"""Repositorio mock en memoria para Orden - sin acceso a BD"""
from datetime import date
from typing import Optional, List, Dict, Any
from unittest.mock import MagicMock


class OrdenRepositoryMock:
    """Repositorio en memoria para Orden. Simula persistencia sin BD real."""
    
    def __init__(self):
        self._ordenes: Dict[int, 'Orden'] = {}
        self._id_counter = 1
    
    def create(self, garantia: int, estadoPago: str, precio: float, fecha: date):
        """Crea una orden simple sin relaciones."""
        from db.models.orden import Orden
        
        orden = Orden(garantia=garantia, estadoPago=estadoPago, precio=precio, fecha=fecha)
        orden.id = self._id_counter
        self._id_counter += 1
        self._ordenes[orden.id] = orden
        return orden
    
    def create_with_services(
        self, 
        garantia: int, 
        estadoPago: str, 
        precio: float, 
        fecha: date,
        servicios: List[Dict[str, Any]],
        empleados: Optional[List[Dict[str, Any]]] = None
    ):
        """Crea una orden con servicios y empleados (sin BD real)."""
        from db.models.orden import Orden
        from db.models.orden_servicio import OrdenServicio
        from db.models.orden_empleado import OrdenEmpleado
        
        if not servicios:
            raise ValueError("La lista de servicios no puede estar vacía")
        
        orden = Orden(garantia=garantia, estadoPago=estadoPago, precio=precio, fecha=fecha)
        orden.id = self._id_counter
        self._id_counter += 1
        
        try:
            # Agregar servicios
            for item in servicios:
                precio_servicio = item.get("precio_servicio")
                if precio_servicio is None:
                    raise ValueError("precio_servicio inválido")
                
                # Crear relación orden-servicio (mock)
                os = MagicMock(spec=OrdenServicio)
                os.orden_id = orden.id
                os.precio_servicio = precio_servicio
                
                orden.agregar_servicio(os)
            
            # Agregar empleados si vienen
            if empleados:
                for item in empleados:
                    oe = MagicMock(spec=OrdenEmpleado)
                    oe.orden_id = orden.id
                    orden.asignar_empleado(oe)
            
            self._ordenes[orden.id] = orden
            return orden
        
        except Exception:
            raise
    
    def get_by_id(self, orden_id: int):
        """Obtiene una orden por ID."""
        return self._ordenes.get(orden_id)
    
    def get_all(self) -> List:
        """Obtiene todas las órdenes."""
        return list(self._ordenes.values())
    
    def save(self, orden):
        """Guarda/actualiza una orden."""
        self._ordenes[orden.id] = orden
        return orden
    
    def delete(self, orden_id: int) -> bool:
        """Elimina una orden."""
        if orden_id in self._ordenes:
            del self._ordenes[orden_id]
            return True
        return False
    
    def reset(self):
        """Reinicia el repositorio (para tests)."""
        self._ordenes.clear()
        self._id_counter = 1
