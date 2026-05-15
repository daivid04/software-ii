from typing import List, Dict

class MockNotificationService:
    """
    Mock genérico para simulaciones de servicios de notificaciones (ej. correos, SMS).
    Sirve como 'Spy' / 'Mock' genérico en las capas de Use Case de Hexagonal Architecture.
    """
    def __init__(self):
        self.sent_messages: List[Dict[str, str]] = []

    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        """Simula enviar un correo"""
        self.sent_messages.append({
            "type": "EMAIL",
            "recipient": recipient,
            "subject": subject,
            "body": body
        })
        return True

    def send_sms(self, phone: str, message: str) -> bool:
        """Simula enviar un SMS"""
        self.sent_messages.append({
            "type": "SMS",
            "recipient": phone,
            "message": message
        })
        return True

    def get_messages_for(self, recipient: str) -> List[Dict[str, str]]:
        return [msg for msg in self.sent_messages if msg["recipient"] == recipient]

    def clear(self):
        self.sent_messages.clear()
