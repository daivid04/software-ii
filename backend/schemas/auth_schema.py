from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    """
    Schema para la solicitud de inicio de sesión.
    
    Attributes:
        email: Correo electrónico del usuario
        password: Contraseña del usuario
    """
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    """
    Schema para la respuesta de inicio de sesión.
    
    Attributes:
        success: Indica si el inicio de sesión fue exitoso
        message: Mensaje descriptivo del resultado
        access_token: Token de acceso (solo si success=True)
        user_email: Email del usuario autenticado (solo si success=True)
    """
    success: bool
    message: str
    access_token: str | None = None
    user_email: str | None = None
