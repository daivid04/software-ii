from pydantic import BaseModel, field_validator
import re


class ProductoBase(BaseModel):
    nombre: str
    descripcion: str
    precio_compra: float
    precio_venta: float
    marca: str
    categoria: str
    stock: int
    stock_minimo: int
    
    @field_validator('nombre', 'descripcion', 'marca', 'categoria')
    @classmethod
    def sanitize_html(cls, v: str) -> str:
        """Prevenir inyección de scripts HTML/JavaScript"""
        if v is None:
            return v
        # Eliminar tags HTML y scripts
        v = re.sub(r'<[^>]*>', '', v)
        # Eliminar caracteres peligrosos
        v = re.sub(r'[<>"\']', '', v)
        return v.strip()


class ProductoCreate(ProductoBase):
    codigo_barras: str | None = None
    img: str | None = None


class ProductoResponse(ProductoBase):
    id: int
    codigo_barras: str | None = None
    img: str | None = None
    tipo: str | None = None

    class Config:
        from_attributes = True