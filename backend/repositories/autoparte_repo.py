from sqlalchemy.orm import Session
from db.models.autoparte import Autoparte
from schemas.autoparte_schema import AutoparteCreate



class AutoparteRepository:

    def __init__(self, db: Session):
        self.db = db
    
    def create(self, autoparte_data: AutoparteCreate):
        autoparte = Autoparte(**autoparte_data.model_dump())
        self.db.add(autoparte)
        self.db.commit()
        self.db.refresh(autoparte)
        return autoparte

    def get_all(self):
        return self.db.query(Autoparte).all()
    
    def get_by_id(self, id: int):
        return self.db.query(Autoparte).filter(Autoparte.id == id).first()
    
    def get_by_name(self, nombre: str):
        return self.db.query(Autoparte).filter(Autoparte.nombre.ilike(nombre)).first()

    def update(self, id: int, autoparte_data: AutoparteCreate):
        autoparte = self.get_by_id(id)
        if not autoparte:
            return None
        data = autoparte_data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(autoparte, key, value)
        self.db.commit()
        self.db.refresh(autoparte)
        return autoparte
    
    def delete(self, id: int):
        autoparte = self.get_by_id(id)
        if autoparte:
            self.db.delete(autoparte)
            self.db.commit()
        return autoparte

    # Métodos específicos para autopartes
    def get_by_modelo(self, modelo: str):
        return self.db.query(Autoparte).filter(Autoparte.modelo == modelo).all()
    
    def get_by_anio(self, anio: int):
        """
        Busca autopartes compatibles con un año específico.
        Funciona con formatos: "2020", "2018-2023", "2018, 2020, 2022"
        """
        anio_str = str(anio)
        # Buscar donde el año aparezca en el string (exacto, en rango o en lista)
        return self.db.query(Autoparte).filter(
            Autoparte.anio.contains(anio_str)
        ).all()