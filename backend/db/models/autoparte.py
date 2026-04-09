from sqlalchemy import Column, Integer, String, ForeignKey
from .producto import Producto



class Autoparte(Producto):
    __tablename__ = "autopartes"
    
    id = Column(Integer, ForeignKey('productos.id'), primary_key=True)
    modelo = Column(String, nullable=False)
    anio = Column(String(50), nullable=False)  # String para soportar rangos: "2018-2023" o listas: "2018, 2020, 2022"
    
    __mapper_args__ = {
        'polymorphic_identity': 'autoparte',
    }