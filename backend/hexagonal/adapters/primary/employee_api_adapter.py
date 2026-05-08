"""
Adaptador Primario (Driving Adapter)
Expone los casos de uso mediante una API REST (FastAPI)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.base import SessionLocal
from schemas.empleado_schema import EmpleadoCreate, EmpleadoResponse
from hexagonal.adapters.secondary.sqlalchemy_employee_repository import SqlAlchemyEmployeeRepository
from hexagonal.usecases.employee_usecase import EmployeeUseCase
from core.auth import require_supabase_user

router = APIRouter(tags=["Empleados - Hexagonal"])

def get_db():
    """Dependencia para obtener la sesión de BD"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_employee_usecase(db: Session = Depends(get_db)) -> EmployeeUseCase:
    """Dependencia para obtener el caso de uso de Empleado"""
    repository = SqlAlchemyEmployeeRepository(db)
    return EmployeeUseCase(repository=repository)

@router.post(
    "/",
    response_model=EmpleadoResponse,
    dependencies=[Depends(require_supabase_user)],
    summary="Crear nuevo empleado (Hexagonal)"
)
def create_empleado(
    data: EmpleadoCreate,
    usecase: EmployeeUseCase = Depends(get_employee_usecase)
):
    """
    Crea un nuevo empleado usando arquitectura hexagonal.
    Requiere autenticación Supabase.
    """
    try:
        employee_dict = data.model_dump()
        result = usecase.create_employee(employee_dict)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/",
    response_model=list[EmpleadoResponse],
    summary="Listar empleados (Hexagonal)"
)
def list_empleados(
    usecase: EmployeeUseCase = Depends(get_employee_usecase)
):
    """
    Lista todos los empleados usando arquitectura hexagonal.
    """
    return usecase.list_employees()

@router.get(
    "/{id}",
    response_model=EmpleadoResponse,
    summary="Obtener empleado por ID (Hexagonal)"
)
def get_empleado(
    id: int,
    usecase: EmployeeUseCase = Depends(get_employee_usecase)
):
    """
    Obtiene un empleado específico por su ID.
    """
    empleado = usecase.get_employee(id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado

@router.put(
    "/{id}",
    response_model=EmpleadoResponse,
    dependencies=[Depends(require_supabase_user)],
    summary="Actualizar empleado (Hexagonal)"
)
def update_empleado(
    id: int,
    data: EmpleadoCreate,
    usecase: EmployeeUseCase = Depends(get_employee_usecase)
):
    """
    Actualiza un empleado existente.
    Requiere autenticación Supabase.
    """
    employee_dict = data.model_dump(exclude_unset=True)
    result = usecase.update_employee(id, employee_dict)
    if not result:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return result

@router.delete(
    "/{id}",
    response_model=EmpleadoResponse,
    dependencies=[Depends(require_supabase_user)],
    summary="Eliminar empleado (Hexagonal)"
)
def delete_empleado(
    id: int,
    usecase: EmployeeUseCase = Depends(get_employee_usecase)
):
    """
    Elimina un empleado existente.
    Requiere autenticación Supabase.
    """
    result = usecase.delete_employee(id)
    if not result:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return result
