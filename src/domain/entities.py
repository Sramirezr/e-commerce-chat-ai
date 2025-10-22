from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


# -----------------------------
# ENTIDAD: PRODUCT
# -----------------------------
@dataclass
class Product:
    """
    Entidad que representa un producto en el e-commerce.
    Contiene la lógica de negocio relacionada con productos.
    """
    id: Optional[int]
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    def __post_init__(self):
        """
        Validaciones que se ejecutan después de crear el objeto.
        """
        if not self.name or not self.name.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        if self.price <= 0:
            raise ValueError("El precio debe ser mayor que 0.")
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo.")

    def is_available(self) -> bool:
        """Retorna True si el producto tiene stock disponible."""
        return self.stock > 0

    def reduce_stock(self, quantity: int) -> None:
        """
        Reduce el stock del producto.
        """
        if quantity <= 0:
            raise ValueError("La cantidad a reducir debe ser positiva.")
        if quantity > self.stock:
            # ✅ corregido para coincidir con el test
            raise ValueError("Stock insuficiente.")
        self.stock -= quantity

    def increase_stock(self, quantity: int) -> None:
        """
        Aumenta el stock del producto.
        """
        if quantity <= 0:
            raise ValueError("La cantidad a aumentar debe ser positiva.")
        self.stock += quantity


# -----------------------------
# ENTIDAD: CHAT MESSAGE
# -----------------------------
@dataclass
class ChatMessage:
    """
    Entidad que representa un mensaje en el chat.
    """
    id: Optional[int]
    session_id: str
    role: str  # 'user' o 'assistant'
    message: str
    timestamp: datetime

    def __post_init__(self):
        """
        Validaciones que se ejecutan después de crear el mensaje.
        """
        if self.role not in {"user", "assistant"}:
            raise ValueError("El rol debe ser 'user' o 'assistant'.")
        if not self.session_id or not self.session_id.strip():
            raise ValueError("El session_id no puede estar vacío.")
        if not self.message or not self.message.strip():
            raise ValueError("El mensaje no puede estar vacío.")

    def is_from_user(self) -> bool:
        """Retorna True si el mensaje fue enviado por el usuario."""
        return self.role == "user"

    def is_from_assistant(self) -> bool:
        """Retorna True si el mensaje fue enviado por el asistente."""
        return self.role == "assistant"


# -----------------------------
# VALUE OBJECT: CHAT CONTEXT
# -----------------------------
@dataclass
class ChatContext:
    """
    Value Object que encapsula el contexto de una conversación.
    Mantiene los mensajes recientes para dar coherencia al chat.
    """
    messages: List[ChatMessage]
    max_messages: int = 6

    def get_recent_messages(self) -> List[ChatMessage]:
        """Retorna los últimos N mensajes (max_messages)."""
        return self.messages[-self.max_messages:]

    def format_for_prompt(self) -> str:
        """
        Formatea los mensajes para incluirlos en el prompt de IA.
        ✅ corregido para usar "assistant" en lugar de "Asistente"
        """
        formatted = []
        for msg in self.get_recent_messages():
            role = "user" if msg.role == "user" else "assistant"
            formatted.append(f"{role}: {msg.message}")
        return "\n".join(formatted)
