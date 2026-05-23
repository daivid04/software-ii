from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.models import Servicio

from schemas.servicio_schema import ServicioCreate

class ServicioRepository:

    def __init__(self, db: Session):
        self.db = db
    
    def registrar_servicio(self, servicio_data: ServicioCreate):
        """Registra un nuevo servicio en el catálogo"""
        servicio = Servicio(**servicio_data.model_dump())
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

    def actualizar_servicio(self, id: int, servicio_data: ServicioCreate):
        """Actualiza la información de un servicio"""
        servicio = self.consultar_servicio(id)
        if not servicio:
            return None
        data = servicio_data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(servicio, key, value)
        self.db.commit()
        self.db.refresh(servicio)
        return servicio
    
    def dar_de_baja_servicio(self, id: int):
        """Da de baja un servicio del catálogo"""
        servicio = self.consultar_servicio(id)
        if servicio:
            try:
                self.db.delete(servicio)
                self.db.commit()
            except IntegrityError as e:
                self.db.rollback()
                raise ValueError(f"No se puede eliminar el servicio porque tiene órdenes o referencias asociadas")
        return servicio