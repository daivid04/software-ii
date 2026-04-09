from fastapi import APIRouter
from schemas.auth_schema import LoginRequest, LoginResponse
from services.auth_service import AuthService

router = APIRouter(tags=["Autenticación"])

@router.post("/login", response_model=LoginResponse, summary="Iniciar sesión")
async def login(credentials: LoginRequest):
    """
    Autentica al usuario en el sistema
    
    Este endpoint verifica las credenciales contra Supabase Auth y **siempre retorna HTTP 200**,
    incluso si las credenciales son incorrectas. El resultado se indica en el campo `success`.
    
    **Validaciones:
    - **Email**: Debe ser un formato válido de correo electrónico
    - **Password**: Campo requerido (mínimo 1 carácter)
    
    **Ejemplo de Request CORRECTO:
    ```json
    {
        "email": "usuario@tallerdiego.com",
        "password": "MiPassword123"
    }
    ```
    
    **Response EXITOSA (credenciales válidas):
    ```json
    {
        "success": true,
        "message": "Inicio de sesión exitoso",
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "user_email": "usuario@tallerdiego.com"
    }
    ```
    **Status:** `200 OK`
    
    **Response FALLIDA (credenciales inválidas):
    ```json
    {
        "success": false,
        "message": "Credenciales inválidas. Por favor, verifica tu email y contraseña.",
        "access_token": null,
        "user_email": null
    }
    ```
    **Status:** `200 OK` (nota: siempre 200, incluso en error)
    
    **Response FALLIDA (error de conexión):
    ```json
    {
        "success": false,
        "message": "Error de conexión con el servicio de autenticación. Intenta nuevamente.",
        "access_token": null,
        "user_email": null
    }
    ```
    **Status:** `200 OK`
    
    **Email con formato inválido:
    ```json
    {
        "email": "no-es-un-email",  // Formato inválido
        "password": "password123"
    }
    ```
    **Error:** `422 Unprocessable Entity`
    ```json
    {
        "detail": [
            {
                "loc": ["body", "email"],
                "msg": "value is not a valid email address",
                "type": "value_error.email"
            }
        ]
    }
    ```
    
    **Comportamiento especial:
    - Este endpoint **NO retorna 400 o 401** para credenciales inválidas
    - Siempre retorna **200 OK** con `success: true/false`
    - Esto mejora la experiencia de usuario al evitar errores visibles en consola
    
    **Autenticación:
    No requiere autenticación previa (endpoint público)
    
    **Uso del token:
    Incluye el `access_token` en requests subsecuentes:
    ```
    Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    ```
    """
    auth_service = AuthService()
    return await auth_service.login(credentials.email, credentials.password)
