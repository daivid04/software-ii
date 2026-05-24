from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.models import Servicio

from schemas.servicio_schema import ServicioCreate

class ServicioRepository:

    def __init__(self, db: Session):
        self.db = db
    
    def guardar(self, servicio: Servicio):
        """Persiste el Agregado completo en la base de datos"""
        self.db.add(servicio)
        self.db.commit()
        self.db.refresh(servicio)
        return servicio
    
    def listar_catalogo_servicios(self):
        """Lista todos los servicios del catálogo"""
        return self.db.query(Servicio).all()
    
    def consultar_servicio(self, id: int):
        """Consulta un servicio por su ID"""
        return self.db.query(Servicio).filter(Servicio.id == id).first()
    
    def buscar_servicio_por_nombre(self, nombre: str):
        """Busca un servicio por nombre"""
        return self.db.query(Servicio).filter(Servicio.nombre.ilike(nombre)).first()

    
    def dar_de_baja_servicio(self, id: int):
        """Da de baja un servicio del catálogo"""
        servicio = self.consultar_servicio(id)
        if servicio:
            try:
                self.db.delete(servicio)
                self.db.commit()
            except IntegrityError:
                self.db.rollback()
                # Lanzamos un error de base de datos claro
                raise ValueError("No se puede eliminar el servicio porque tiene órdenes o referencias asociadas")
        return servicio