import httpx
from core.config import settings
from schemas.auth_schema import LoginResponse

class AuthService:
    """
    Servicio de autenticación que actúa como intermediario entre el frontend
    y Supabase Auth, manejando errores y devolviendo respuestas consistentes.
    """

    def __init__(self):
        self.supabase_url = settings.SUPABASE_URL.rstrip("/")
        self.anon_key = settings.SUPABASE_ANON_KEY

    async def login(self, email: str, password: str) -> LoginResponse:
        """
        Autentica un usuario contra Supabase Auth.
        
        Args:
            email: Correo electrónico del usuario
            password: Contraseña del usuario
            
        Returns:
            LoginResponse con el resultado de la autenticación
        """
        if not self.supabase_url or not self.anon_key:
            return LoginResponse(
                success=False,
                message="Configuración de autenticación incompleta"
            )

        auth_endpoint = f"{self.supabase_url}/auth/v1/token?grant_type=password"
        
        headers = {
            "apikey": self.anon_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "email": email,
            "password": password
        }

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(
                    auth_endpoint,
                    headers=headers,
                    json=payload
                )
                
                # Si las credenciales son incorrectas (400, 401, etc.)
                if response.status_code != 200:
                    return LoginResponse(
                        success=False,
                        message="Credenciales inválidas. Por favor, verifica tu email y contraseña."
                    )
                
                # Login exitoso
                data = response.json()
                return LoginResponse(
                    success=True,
                    message="Inicio de sesión exitoso",
                    access_token=data.get("access_token"),
                    user_email=data.get("user", {}).get("email")
                )
                
        except httpx.RequestError as e:
            return LoginResponse(
                success=False,
                message=f"Error de conexión con el servicio de autenticación: {str(e)}"
            )
        except Exception as e:
            return LoginResponse(
                success=False,
                message=f"Error inesperado durante la autenticación: {str(e)}"
            )
