from typing import Dict, Any, Optional

class MockExternalApiClient:
    """
    Mock genérico para simulaciones de APIS externas (ej. pasarelas de pago, consultas de facturación electrónica).
    Actúa como un stub para no hacer peticiones HTTP reales durante las pruebas de la arquitectura hexagonal.
    """
    def __init__(self):
        self.responses = {}
        self.call_history = []
        self.network_error = False

    def configure_response(self, endpoint: str, method: str, status_code: int, data: Dict[str, Any]):
        """Configura una respuesta prefijada para un endpoint específico."""
        self.responses[(endpoint, method.upper())] = {
            "status_code": status_code,
            "data": data
        }

    def simulate_network_error(self, active: bool = True):
        self.network_error = active

    def request(self, method: str, endpoint: str, payload: Optional[Dict] = None) -> Dict[str, Any]:
        """Simula una llamada a la API que retorna los datos configurados."""
        self.call_history.append({"method": method, "endpoint": endpoint, "payload": payload})
        
        if self.network_error:
            raise ConnectionError("Network error simulated by MockExternalApiClient")

        response = self.responses.get((endpoint, method.upper()))
        if response:
            if response["status_code"] >= 400:
                # Simular lanzar un error si queremos, u obligar a manejar el payload HTTP
                pass
            return response

        # Comportamiento por defecto si no hay respuesta configurada
        return {"status_code": 200, "data": {"message": "Success (Mocked)"}}
