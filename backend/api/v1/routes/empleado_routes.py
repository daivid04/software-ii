from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.base import SessionLocal
from schemas.empleado_schema import EmpleadoCreate, EmpleadoResponse
from services.empleado_service import EmpleadoService
from core.auth import require_supabase_user

router = APIRouter(tags=["Empleados"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_empleado_service(db: Session = Depends(get_db)) -> EmpleadoService:
    return EmpleadoService(db)

@router.post("/", response_model=EmpleadoResponse, dependencies=[Depends(require_supabase_user)], summary="Registrar nuevo empleado")
def registrar_nuevo_empleado(
    data: EmpleadoCreate,
    service: EmpleadoService = Depends(get_empleado_service)
):
    """
    Registra un nuevo empleado del taller.
    
    Los empleados pueden ser asignados a órdenes de trabajo para rastrear quién realizó cada servicio.
    
    **Validaciones:**
    - Nombre: Mínimo 3 caracteres, máximo 200
    - Puesto: Mínimo 3 caracteres, máximo 100
    - Teléfono: Formato válido (opcional)
    - Email: Formato válido (opcional)
    
    **Ejemplo de Request correcto:**
    ```json
    {
        "nombre": "Carlos Méndez",
        "puesto": "Mecánico Senior",
        "telefono": "555-1234",
        "email": "carlos@tallerdiego.com"
    }
    ```
    
    **Response exitosa:**
    ```json
    {
        "id": 3,
        "nombre": "Carlos Méndez",
        "puesto": "Mecánico Senior",
        "telefono": "555-1234",
        "email": "carlos@tallerdiego.com"
    }
    ```
    
    **Autenticación:**
    Requiere token JWT en header: `Authorization: Bearer <token>`
    """
    return service.registrar_nuevo_empleado(data)

@router.get("/", response_model=list[EmpleadoResponse], summary="Obtener catálogo completo de empleados")
def obtener_catalogo_completo(
    service: EmpleadoService = Depends(get_empleado_service)
):
    """
    Obtiene el listado completo de empleados del taller.
    
    **Response exitosa:**
    ```json
    [
        {
            "id": 3,
            "nombre": "Carlos Méndez",
            "puesto": "Mecánico Senior",
            "telefono": "555-1234",
            "email": "carlos@tallerdiego.com"
        },
        {
            "id": 2,
            "nombre": "Ana Torres",
            "puesto": "Técnico Eléctrico",
            "telefono": "555-5678",
            "email": null
        }
    ]
    ```
    
    **Autenticación:**
    No requiere autenticación (público)
    """
    return service.obtener_catalogo_completo()

@router.get("/{id}", response_model=EmpleadoResponse, summary="Consultar empleado activo")
def consultar_empleado_activo(id: int, service: EmpleadoService = Depends(get_empleado_service)):
    """
    Obtiene un empleado específico activo por su ID.
    
    **Parámetros:**
    - id: ID único del empleado
    
    **Response exitosa:**
    ```json
    {
        "id": 3,
        "nombre": "Carlos Méndez",
        "puesto": "Mecánico Senior",
        "telefono": "555-1234",
        "email": "carlos@tallerdiego.com"
    }
    ```
    
    **Empleado no encontrado:**
    ```json
    {
        "detail": "Empleado no encontrado"
    }
    ```
    Status: `404 Not Found`
    
    **Autenticación:**
    No requiere autenticación (público)
    """
    empleado = service.consultar_empleado_activo(id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado

@router.put("/{id}", response_model=EmpleadoResponse, dependencies=[Depends(require_supabase_user)], summary="Actualizar información de empleado")
def actualizar_empleado(
    id: int,
    data: EmpleadoCreate,
    service: EmpleadoService = Depends(get_empleado_service)
):
    """
    Actualiza la información de un empleado existente.
    
    **Parámetros:**
    - id: ID del empleado a actualizar
    - data: Nuevos datos del empleado (mismo formato que crear empleado)
    
    **Response exitosa:**
    Retorna el empleado actualizado con los nuevos valores.
    
    **Errores:**
    - 404 Not Found: Si el empleado no existe
    
    **Autenticación:**
    Requiere token JWT en header: `Authorization: Bearer <token>`
    """
    empleado = service.actualizar_empleado(id, data)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado

@router.delete("/{id}", dependencies=[Depends(require_supabase_user)], summary="Dar de baja empleado")
def dar_de_baja_empleado(id: int, service: EmpleadoService = Depends(get_empleado_service)):
    """
    Da de baja un empleado del sistema.
    
    **Parámetros:**
    - id: ID del empleado a eliminar
    
    **Response exitosa:**
    ```json
    {
        "detail": "Empleado eliminado"
    }
    ```
    
    **Errores:**
    - 404 Not Found: Si el empleado no existe
    - 409 Conflict: Si el empleado está asignado a órdenes activas
    
    **Autenticación:**
    Requiere token JWT en header: `Authorization: Bearer <token>`

    Raises:
        HTTPException(404): Si el empleado no existe.
    """
    empleado = service.dar_de_baja_empleado(id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return {"detail": "Empleado eliminado"}