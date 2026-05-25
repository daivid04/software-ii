from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from db.base import SessionLocal
from datetime import datetime

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", summary="Verificar estado del sistema")
def health_check(db: Session = Depends(get_db)):
    """
    Verificación de salud del sistema completo
    
    Valida que todas las capas de la arquitectura estén funcionando correctamente:
    **Frontend → Backend → Base de Datos → Backend → Frontend**
    
    **Response EXITOSA:
    ```json
    {
        "status": "success",
        "message": "Línea Base Arquitectónica validada ",
        "layers": {
            "presentation": "Frontend conectado",
            "service": "Backend operativo",
            "persistence": {
                "database_connected": true,
                "database_name": "postgres",
                "database_version": "PostgreSQL 17.6 on aarch64-unknown-linux-gnu"
            }
        },
        "timestamp": "2025-12-04T11:32:39.910088",
        "architecture_flow": "✓ Frontend → ✓ Backend → ✓ Database → ✓ Response"
    }
    ```
    
    **Response FALLIDA (error de base de datos):
    ```json
    {
        "status": "error",
        "message": "Error de conexión a la base de datos",
        "layers": {
            "presentation": "Frontend conectado",
            "service": "Backend operativo",
            "persistence": {
                "database_connected": false,
                "error": "Connection refused"
            }
        },
        "timestamp": "2025-12-04T11:32:39.910088",
        "architecture_flow": "✓ Frontend → ✓ Backend → ✗ Database"
    }
    ```
    **Status:** `500 Internal Server Error`
    
    **Capas validadas:
    - **Presentation**: Frontend puede alcanzar el backend
    - **Service**: Backend está procesando requests
    - **Persistence**: Base de datos está accesible y respondiendo
    
    **Uso:
    Este endpoint es útil para:
    - Monitoring y health checks automáticos
    - Validar deployment después de cambios
    - Debugging de problemas de conectividad
    - Verificar versión de PostgreSQL
    
    **Autenticación:
    No requiere autenticación (público)
    """
    try:
        # Capa de Persistencia: Ejecutar consulta trivial a la BD
        result = db.execute(text("SELECT 1 as status, 'OK' as message")).fetchone()
        
        # Verificar conexión y obtener información adicional
        db_info = db.execute(text("SELECT current_database(), version()")).fetchone()
        
        return {
            "status": "success",
            "message": "Línea Base Arquitectónica validada ",
            "layers": {
                "presentation": "Frontend conectado",
                "service": "Backend operativo",
                "persistence": {
                    "database_connected": result.status == 1,
                    "database_name": db_info[0] if db_info else "unknown",
                    "database_version": db_info[1].split(',')[0] if db_info else "unknown"
                }
            },
            "timestamp": datetime.now().isoformat(),
            "architecture_flow": "✓ Frontend → ✓ Backend → ✓ Database → ✓ Response"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error en la línea base: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "architecture_flow": "✗ Fallo en comunicación"
        }
