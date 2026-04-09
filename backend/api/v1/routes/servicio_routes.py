from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.base import SessionLocal
from schemas.servicio_schema import ServicioCreate, ServicioResponse
from services.servicio_service import ServicioService
from core.auth import require_supabase_user

router = APIRouter(tags=["Servicios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_servicio_service(db: Session = Depends(get_db)) -> ServicioService:
    return ServicioService(db)

@router.post("/", response_model=ServicioResponse, dependencies=[Depends(require_supabase_user)], summary="Crear nuevo servicio")
def create_servicio(
    data: ServicioCreate,
    service: ServicioService = Depends(get_servicio_service)
):
    """
    Crea un nuevo servicio ofrecido por el taller.
    
    Los servicios representan trabajos mecánicos que pueden ser asignados a órdenes.
    
    **Validaciones:**
    - Nombre: Mínimo 3 caracteres, máximo 200
    - Descripción: Mínimo 10 caracteres, máximo 500
    - Precio: Debe ser mayor a 0
    
    **Ejemplo de Request correcto:**
    ```json
    {
        "nombre": "Cambio de aceite y filtro",
        "descripcion": "Servicio completo de cambio de aceite sintético y reemplazo de filtro de aceite",
        "precio": 150.00
    }
    ```
    
    **Response exitosa:**
    ```json
    {
        "id": 5,
        "nombre": "Cambio de aceite y filtro",
        "descripcion": "Servicio completo de cambio de aceite sintético...",
        "precio": 150.00
    }
    ```
    
    **Autenticación:**
    Requiere token JWT en header: `Authorization: Bearer <token>`
    """
    try:
        return service.create_servicio(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[ServicioResponse], summary="Listar todos los servicios")
def list_servicios(
    service: ServicioService = Depends(get_servicio_service)
):
    """
    Obtiene el catálogo completo de servicios disponibles.
    
    Retorna todos los servicios que el taller puede ofrecer y que pueden ser asignados a órdenes de trabajo.
    
    **Response exitosa:**
    ```json
    [
        {
            "id": 5,
            "nombre": "Cambio de aceite y filtro",
            "descripcion": "Servicio completo de cambio de aceite...",
            "precio": 150.00
        },
        {
            "id": 12,
            "nombre": "Alineación y balanceo",
            "descripcion": "Alineación computarizada y balanceo de 4 ruedas",
            "precio": 80.00
        }
    ]
    ```
    
    **Autenticación:**
    No requiere autenticación (público)
    """
    return service.list_servicios()

@router.get("/{id}", response_model=ServicioResponse, summary="Obtener servicio por ID")
def get_servicio(id: int, service: ServicioService = Depends(get_servicio_service)):
    """
    Obtiene un servicio específico por su ID.
    
    **Parámetros:**
    - id: ID único del servicio
    
    **Response exitosa:**
    ```json
    {
        "id": 5,
        "nombre": "Cambio de aceite y filtro",
        "descripcion": "Servicio completo de cambio de aceite sintético...",
        "precio": 150.00
    }
    ```
    
    **Servicio no encontrado:**
    ```json
    {
        "detail": "Servicio no encontrado"
    }
    ```
    Status: `404 Not Found`
    
    **Autenticación:**
    No requiere autenticación (público)
    """
    servicio = service.get_by_id(id)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio

@router.put("/{id}", response_model=ServicioResponse, dependencies=[Depends(require_supabase_user)], summary="Actualizar servicio")
def update_servicio(
    id: int,
    data: ServicioCreate,
    service: ServicioService = Depends(get_servicio_service)
):
    """
    Actualiza la información de un servicio existente.
    
    **Parámetros:**
    - id: ID del servicio a actualizar
    - data: Nuevos datos del servicio (mismo formato que crear servicio)
    
    **Response exitosa:**
    Retorna el servicio actualizado con los nuevos valores.
    
    **Errores:**
    - 404 Not Found: Si el servicio no existe
    - 400 Bad Request: Si los datos no cumplen las validaciones
    
    **Autenticación:**
    Requiere token JWT en header: `Authorization: Bearer <token>`
    """
    try:
        servicio = service.update_servicio(id, data)
        if not servicio:
            raise HTTPException(status_code=404, detail="Servicio no encontrado")
        return servicio
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id}", dependencies=[Depends(require_supabase_user)], summary="Eliminar servicio", description="Elimina un servicio del sistema.")
def delete_servicio(id: int, service: ServicioService = Depends(get_servicio_service)):
    """
    Elimina un servicio por su ID.

    Args:
        id: ID del servicio a eliminar.

    Returns:
        dict: Mensaje de confirmación.

    Raises:
        HTTPException(404): Si el servicio no existe.
        HTTPException(409): Si no se puede eliminar (ej. tiene dependencias).
    """
    try:
        servicio = service.delete_servicio(id)
        if not servicio:
            raise HTTPException(status_code=404, detail="Servicio no encontrado")
        return {"detail": "Servicio eliminado"}
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))