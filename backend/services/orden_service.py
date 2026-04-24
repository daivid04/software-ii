from sqlalchemy.orm import Session
from repositories.orden_repo import OrdenRepository
from schemas.orden_schema import OrdenCreate
from fastapi import HTTPException
from db.models.orden import Orden
from db.models.orden_servicio import OrdenServicio
from db.models.orden_empleado import OrdenEmpleado
from core.value_objects import Precio, EstadoPago, Garantia


class OrdenService:
    """
    Servicio de Orden de Trabajo
    
    Coordina la creación y manipulación de órdenes.
    Delega la validación de reglas de negocio al Aggregate Root (Orden).
    """
    
    def __init__(self, db: Session):
        self.repo = OrdenRepository(db)

    def create_orden(self, data: OrdenCreate):
        """
        Crea una nueva orden de trabajo.
        
        Valida que los servicios y empleados existan antes de crear la orden.
        Luego usa los métodos del Aggregate Root para manipular la orden.
        
        Args:
            data: Datos de la orden a crear
            
        Returns:
            Orden creada
            
        Raises:
            HTTPException: Si hay validaciones fallidas
        """
        try:
            # Validar precio inicial usando Value Object
            Precio(float(data.precio))
            
            # Validar estado de pago usando Value Object
            EstadoPago(data.estadoPago)
            
            # Validar garantía usando Value Object
            Garantia(data.garantia)

            servicios = getattr(data, "servicios", None)
            empleados = getattr(data, "empleados", None)

            servicios_list = [p.model_dump() if hasattr(p, 'model_dump') else p for p in servicios] if servicios else []
            empleados_list = [p.model_dump() if hasattr(p, 'model_dump') else p for p in empleados] if empleados else []

            # Si hay servicios o empleados asociados, crear con relaciones
            if servicios_list or empleados_list:
                try:
                    return self.repo.create_with_services(
                        data.garantia,
                        data.estadoPago,
                        data.precio,
                        data.fecha,
                        servicios_list,
                        empleados_list,
                    )
                except ValueError as e:
                    raise HTTPException(status_code=400, detail=str(e))

            # Caso simple: solo la orden
            return self.repo.create(data.garantia, data.estadoPago, data.precio, data.fecha)
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def list_ordens(self):
        """Obtiene todas las órdenes."""
        return self.repo.get_all()

    def get_by_id(self, id: int):
        """Obtiene una orden por ID."""
        return self.repo.get_by_id(id)

    def get_by_fecha(self, fecha):
        """Obtiene órdenes por fecha."""
        return self.repo.get_by_fecha(fecha)

    def cambiar_estado_pago(self, id: int, nuevo_estado: str) -> Orden:
        """
        Cambia el estado de pago de una orden existente.
        
        Usa el método del Aggregate Root para validar el cambio.
        
        Args:
            id: ID de la orden
            nuevo_estado: Nuevo estado ("pendiente", "parcial", "completado")
            
        Returns:
            Orden actualizada
            
        Raises:
            HTTPException: Si la orden no existe o el estado es inválido
        """
        orden = self.repo.get_by_id(id)
        if not orden:
            raise HTTPException(status_code=404, detail="Orden no encontrada")
        
        try:
            orden.cambiar_estado_pago(nuevo_estado)
            self.repo.save(orden)
            return orden
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def delete_orden(self, id: int):
        """Elimina una orden."""
        return self.repo.delete(id)