from pydantic import BaseModel
from datetime import datetime
from schemas.producto_schema import ProductoResponse



class VentaBase(BaseModel):
    fecha: datetime



class VentaProductoBase(BaseModel):
    producto_id: int
    cantidad: int

 

class VentaProductoResponse(VentaProductoBase):
    producto: ProductoResponse | None = None

    class Config:
        from_attributes = True



class VentaCreate(VentaBase):
    productos: list[VentaProductoBase] | None = []



class VentaResponse(VentaBase):
    id: int
    productos: list[VentaProductoResponse] | None = None

    class Config:
        from_attributes = True