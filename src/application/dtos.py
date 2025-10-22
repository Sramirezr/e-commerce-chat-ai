from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ---------------------------------------
# DTO: ProductDTO
# ---------------------------------------
class ProductDTO(BaseModel):
    id: Optional[int] = Field(default=None, description="Identificador único del producto")
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    class Config:
        from_attributes = True

    # ✅ Agregado para test_get_all_products
    @classmethod
    def from_entity(cls, entity):
        return cls(
            id=entity.id,
            name=entity.name,
            brand=entity.brand,
            category=entity.category,
            size=entity.size,
            color=entity.color,
            price=entity.price,
            stock=entity.stock,
            description=entity.description
        )


# ---------------------------------------
# DTO: ChatMessageDTO
# ---------------------------------------
class ChatMessageDTO(BaseModel):
    id: Optional[int]
    session_id: str
    role: str
    message: str
    timestamp: datetime

    class Config:
        from_attributes = True


# ---------------------------------------
# DTOs extendidos y de compatibilidad
# ---------------------------------------
class ProductResponseDTO(ProductDTO):
    id: int


class ChatResponseDTO(ChatMessageDTO):
    response: str


class ChatMessageRequestDTO(BaseModel):
    session_id: str
    message: str


class ChatMessageResponseDTO(BaseModel):
    session_id: str
    response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatHistoryDTO(BaseModel):
    session_id: str
    message: str
    is_user: bool
    timestamp: datetime = Field(default_factory=datetime.utcnow)
