from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.models.autoparte import Autoparte
from schemas.autoparte_schema import AutoparteCreate    



class AutoparteRepository:

    def __init__(self, db: Session):
        self.db = db

    # --- NUEVO MÉTODO PARA DDD ---
    def guardar(self, autoparte: Autoparte):
        """Persiste los cambios del Agregado completo en la base de datos"""
        self.db.add(autoparte)
        self.db.commit()
        self.db.refresh(autoparte)
        return autoparte
    
    def registrar_autoparte(self, autoparte_data: AutoparteCreate):
        """Registra una nueva autoparte en el catálogo""" 
        autoparte = Autoparte(**autoparte_data.model_dump())
        return self.guardar(autoparte)

    def listar_catalogo_autopartes(self):
        """Lista todas las autopartes del catálogo"""
        return self.db.query(Autoparte).all()
    
    def consultar_autoparte(self, id: int):
        """Consulta una autoparte por su ID"""
        return self.db.query(Autoparte).filter(Autoparte.id == id).first()
    
    def buscar_autoparte_por_nombre(self, nombre: str):
        """Busca una autoparte por nombre"""
        return self.db.query(Autoparte).filter(Autoparte.nombre.ilike(nombre)).first()


    def actualizar_autoparte(self, autoparte: Autoparte):
        """Actualiza la información de una autoparte"""
        """Ahora recibe el Agregado validado por el dominio y lo persiste"""
        return self.guardar(autoparte)
    
    def dar_de_baja_autoparte(self, id: int):
        """Da de baja una autoparte del catálogo"""
        autoparte = self.consultar_autoparte(id)
        if autoparte:
            try:
                self.db.delete(autoparte)
                self.db.commit()
            except IntegrityError as e:
                self.db.rollback()
                raise ValueError("No se puede dar de baja porque tiene referencias asociadas")
        return autoparte

    # Métodos específicos para autopartes
    def buscar_autopartes_por_modelo(self, modelo: str):
        """Busca autopartes por modelo de vehículo"""
        return self.db.query(Autoparte).filter(Autoparte.modelo == modelo).all()
    
    def buscar_autopartes_por_anio(self, anio: int):
        """
        Busca autopartes compatibles con un año específico.
        Funciona con formatos: "2020", "2018-2023", "2018, 2020, 2022"
        """
        anio_str = str(anio)
        # Buscar donde el año aparezca en el string (exacto, en rango o en lista)
        return self.db.query(Autoparte).filter(Autoparte.anio.contains(anio_str)).all()