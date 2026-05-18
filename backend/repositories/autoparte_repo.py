from sqlalchemy.orm import Session
from db.models.autoparte import Autoparte
from schemas.autoparte_schema import AutoparteCreate



class AutoparteRepository:

    def __init__(self, db: Session):
        self.db = db
    
    def registrar_autoparte(self, autoparte_data: AutoparteCreate):
        """Registra una nueva autoparte en el catálogo"""
        autoparte = Autoparte(**autoparte_data.model_dump())
        self.db.add(autoparte)
        self.db.commit()
        self.db.refresh(autoparte)
        return autoparte

    def listar_catalogo_autopartes(self):
        """Lista todas las autopartes del catálogo"""
        return self.db.query(Autoparte).all()
    
    def consultar_autoparte(self, id: int):
        """Consulta una autoparte por su ID"""
        return self.db.query(Autoparte).filter(Autoparte.id == id).first()
    
    def buscar_autoparte_por_nombre(self, nombre: str):
        """Busca una autoparte por nombre"""
        return self.db.query(Autoparte).filter(Autoparte.nombre.ilike(nombre)).first()

    def actualizar_autoparte(self, id: int, autoparte_data: AutoparteCreate):
        """Actualiza la información de una autoparte"""
        autoparte = self.consultar_autoparte(id)
        if not autoparte:
            return None
        data = autoparte_data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(autoparte, key, value)
        self.db.commit()
        self.db.refresh(autoparte)
        return autoparte
    
    def dar_de_baja_autoparte(self, id: int):
        """Da de baja una autoparte del catálogo"""
        autoparte = self.consultar_autoparte(id)
        if autoparte:
            self.db.delete(autoparte)
            self.db.commit()
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
        return self.db.query(Autoparte).filter(
            Autoparte.anio.contains(anio_str)
        ).all()