from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.models import Producto
from schemas.producto_schema import ProductoCreate



class ProductoRepository:

    def __init__(self, db: Session):
        self.db = db
    
    def create(self, producto_data: ProductoCreate):
        producto = Producto(**producto_data.model_dump())
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def get_all(self):
        return self.db.query(Producto).all()
    
    def get_by_id(self, id: int):
        return self.db.query(Producto).filter(Producto.id == id).first()
    
    def get_by_name(self, nombre: str):
        return self.db.query(Producto).filter(Producto.nombre.ilike(nombre)).first()
    
    def get_by_barcode(self, codBarras: str):
        return self.db.query(Producto).filter(Producto.codBarras == codBarras).first()

    def update(self, id: int, producto_data: ProductoCreate):
        producto = self.get_by_id(id)
        if not producto:
            return None
        data = producto_data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(producto, key, value)
        self.db.commit()
        self.db.refresh(producto)
        return producto
    
    def delete(self, id: int):
        producto = self.get_by_id(id)
        if producto:
            try:
                self.db.delete(producto)
                self.db.commit()
            except IntegrityError as e:
                self.db.rollback()
                # Si hay un error de integridad (ej: ventas asociadas), lanzar una excepción más clara
                raise ValueError(f"No se puede eliminar el producto porque tiene ventas o referencias asociadas")
        return producto