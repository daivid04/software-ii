from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import httpx

from core.config import settings

_bearer_scheme = HTTPBearer(auto_error=False)


async def require_supabase_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
):
    """Validate Supabase JWT and return the authenticated user profile."""
    if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Configuración de Supabase incompleta",
        )

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación requerido",
        )

    headers = {
        "apikey": settings.SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {credentials.credentials}",
    }
    user_endpoint = settings.SUPABASE_URL.rstrip("/") + "/auth/v1/user"

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(user_endpoint, headers=headers)
    except httpx.RequestError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"No se pudo validar el token con Supabase: {error}",
        ) from error

    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Supabase inválido o expirado",
        )

    return response.json()
