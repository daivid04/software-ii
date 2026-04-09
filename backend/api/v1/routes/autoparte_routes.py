from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.base import SessionLocal
from schemas.autoparte_schema import AutoparteCreate, AutoparteResponse
from services.autoparte_service import AutoparteService
from core.auth import require_supabase_user

router = APIRouter(tags=["Autopartes"])



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

 

def get_autoparte_service(db: Session = Depends(get_db)) -> AutoparteService:
    return AutoparteService(db)

@router.post("/", response_model=AutoparteResponse, dependencies=[Depends(require_supabase_user)], summary="Crear nueva autoparte")
def create_autoparte(
    data: AutoparteCreate,
    service: AutoparteService = Depends(get_autoparte_service)
):
    """
    Crea una nueva autoparte en el inventario
    
    Las autopartes son productos específicos para vehículos con campos adicionales.
    
    **Validaciones:
    - **Nombre**: Mínimo 3 caracteres, máximo 200
    - **Marca**: Mínimo 2 caracteres, máximo 100
    - **Descripción**: Mínimo 10 caracteres, máximo 500
    - **Precio de venta**: Debe ser mayor al precio de compra
    - **Stock**: No puede ser negativo
    - **Año**: Formato flexible (ej: "2020", "2018-2023", "2015, 2017, 2019")
    - **Código de barras**: Único en el sistema
    
    **Ejemplo de Request CORRECTO:
    ```json
    {
        "nombre": "Filtro de Aire K&N",
        "marca": "K&N",
        "descripcion": "Filtro de aire deportivo de alto flujo, reutilizable y lavable, aumenta potencia del motor",
        "precio_compra": 450.00,
        "precio_venta": 750.00,
        "stock": 15,
        "imagen_url": "https://example.com/filtro-kn.jpg",
        "cod_barras": "T-A196-FIL",
        "modelo": "33-2304",
        "anio": "2015-2023",
        "motor": "1.6L, 2.0L",
        "aplicacion": "Honda Civic, CR-V"
    }
    ```
    
    **Response EXITOSA:
    ```json
    {
        "id": 196,
        "nombre": "Filtro de Aire K&N",
        "marca": "K&N",
        "descripcion": "Filtro de aire deportivo de alto flujo...",
        "precio_compra": 450.00,
        "precio_venta": 750.00,
        "stock": 15,
        "imagen_url": "https://example.com/filtro-kn.jpg",
        "cod_barras": "T-A196-FIL",
        "tipo": "autoparte",
        "modelo": "33-2304",
        "anio": "2015-2023",
        "motor": "1.6L, 2.0L",
        "aplicacion": "Honda Civic, CR-V"
    }
    ```
    
    **Ejemplos de Requests INCORRECTOS:
    
    **1. Precio de venta menor o igual al de compra:**
    ```json
    {
        "nombre": "Autoparte Test",
        "precio_compra": 500.00,
        "precio_venta": 450.00  // Debe ser > precio_compra
    }
    ```
    **Error:** `400 Bad Request - "Precio de venta debe ser mayor al precio de compra"`
    
    **2. Descripción muy corta:**
    ```json
    {
        "nombre": "Autoparte Test",
        "descripcion": "Corta"  // Mínimo 10 caracteres
    }
    ```
    **Error:** `400 Bad Request - "La descripción debe tener al menos 10 caracteres"`
    
    **3. Código de barras duplicado:**
    ```json
    {
        "nombre": "Autoparte Test",
        "cod_barras": "T-A196-FIL"  // Ya existe
    }
    ```
    **Error:** `400 Bad Request - "El código de barras ya existe"`
    
    **📝 Nota sobre el campo "año":
    Acepta múltiples formatos:
    - Año único: `"2020"`
    - Rango: `"2018-2023"`
    - Lista: `"2015, 2017, 2019"`
    
    **Autenticación:
    Requiere token JWT en header: `Authorization: Bearer <token>`
    """
    return service.create_autoparte(data)


@router.get("/", response_model=list[AutoparteResponse], summary="Listar todas las autopartes")
def list_autopartes(
    service: AutoparteService = Depends(get_autoparte_service)
):
    """
    Obtiene el listado completo de autopartes
    
    Retorna todas las autopartes registradas en el inventario.
    Las autopartes incluyen información específica para vehículos (modelo, año, motor, aplicación).
    
    **Response EXITOSA:
    ```json
    [
        {
            "id": 196,
            "nombre": "Filtro de Aire K&N",
            "marca": "K&N",
            "descripcion": "Filtro de aire deportivo...",
            "precio_compra": 450.00,
            "precio_venta": 750.00,
            "stock": 15,
            "imagen_url": "https://example.com/filtro-kn.jpg",
            "cod_barras": "T-A196-FIL",
            "tipo": "autoparte",
            "modelo": "33-2304",
            "anio": "2015-2023",
            "motor": "1.6L, 2.0L",
            "aplicacion": "Honda Civic, CR-V"
        },
        {
            "id": 195,
            "nombre": "Pastillas de Freno Brembo",
            "marca": "Brembo",
            "descripcion": "Pastillas cerámicas premium...",
            "precio_compra": 800.00,
            "precio_venta": 1200.00,
            "stock": 8,
            "imagen_url": null,
            "cod_barras": "T-A195-FRE",
            "tipo": "autoparte",
            "modelo": "P28046",
            "anio": "2018-2024",
            "motor": "Todos",
            "aplicacion": "Toyota Corolla"
        }
    ]
    ```
    
    **Campos adicionales en autopartes:
    - **modelo**: Número de modelo de la autoparte
    - **anio**: Año(s) de aplicación del vehículo
    - **motor**: Tipo(s) de motor compatible(s)
    - **aplicacion**: Vehículo(s) compatible(s)
    - **tipo**: Siempre "autoparte"
    
    **Autenticación:
    No requiere autenticación (público)
    """
    return service.list_autopartes()


@router.get("/{id}", response_model=AutoparteResponse, summary="Obtener autoparte por ID", description="Busca una autoparte específica usando su ID único.")
def get_autoparte(id: int, service: AutoparteService = Depends(get_autoparte_service)):
    """
    Obtiene los detalles de una autoparte por su ID.

    Args:
        id: ID único de la autoparte.

    Returns:
        AutoparteResponse: La autoparte encontrada.

    Raises:
        HTTPException(404): Si la autoparte no existe.
    """
    autoparte = service.get_by_id(id)
    if not autoparte:
        raise HTTPException(status_code=404, detail="Autoparte no encontrada")
    return autoparte


@router.put("/{id}", response_model=AutoparteResponse, dependencies=[Depends(require_supabase_user)], summary="Actualizar autoparte", description="Actualiza los datos de una autoparte existente.")
def update_autoparte(
    id: int,
    data: AutoparteCreate,
    service: AutoparteService = Depends(get_autoparte_service)
):
    """
    Actualiza la información de una autoparte existente.

    Args:
        id: ID de la autoparte a actualizar.
        data: Nuevos datos de la autoparte.

    Returns:
        AutoparteResponse: La autoparte actualizada.

    Raises:
        HTTPException(404): Si la autoparte no existe.
    """
    autoparte = service.update_autoparte(id, data)
    if not autoparte:
        raise HTTPException(status_code=404, detail="Autoparte no encontrada")
    return autoparte


@router.delete("/{id}", dependencies=[Depends(require_supabase_user)], summary="Eliminar autoparte", description="Elimina una autoparte del sistema.")
def delete_autoparte(id: int, service: AutoparteService = Depends(get_autoparte_service)):
    """
    Elimina una autoparte por su ID.

    Args:
        id: ID de la autoparte a eliminar.

    Returns:
        dict: Mensaje de confirmación.

    Raises:
        HTTPException(404): Si la autoparte no existe.
    """
    autoparte = service.delete_autoparte(id)
    if not autoparte:
        raise HTTPException(status_code=404, detail="Autoparte no encontrada")
    return {"detail": "Autoparte eliminada"}


# Endpoints específicos para autopartes
@router.get("/modelo/{modelo}", response_model=list[AutoparteResponse], summary="Buscar autopartes por modelo", description="Busca autopartes compatibles con un modelo de vehículo específico.")
def get_autopartes_by_modelo(
    modelo: str,
    service: AutoparteService = Depends(get_autoparte_service)
):
    """
    Busca autopartes por modelo de vehículo.

    Args:
        modelo: Nombre del modelo del vehículo.

    Returns:
        list[AutoparteResponse]: Lista de autopartes compatibles.
    """
    return service.get_by_modelo(modelo)


@router.get("/anio/{anio}", response_model=list[AutoparteResponse], summary="Buscar autopartes por año", description="Busca autopartes compatibles con un año de vehículo específico.")
def get_autopartes_by_anio(
    anio: int,  # El usuario busca con un año numérico (ej: 2020)
    service: AutoparteService = Depends(get_autoparte_service)
):
    """
    Busca autopartes compatibles con un año específico.

    Args:
        anio: Año del vehículo (ej: 2020).

    Returns:
        list[AutoparteResponse]: Lista de autopartes compatibles.
    """
    return service.get_by_anio(anio)