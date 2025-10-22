from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from datetime import datetime
from src.infrastructure.db.database import Base


# ------------------------------
# MODELO: ProductModel
# ------------------------------
class ProductModel(Base):
    """
    Representa un producto almacenado en la base de datos.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, index=True)
    brand = Column(String(100), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    size = Column(String(20), nullable=False)
    color = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f"<ProductModel id={self.id} name={self.name} brand={self.brand}>"


# ------------------------------
# MODELO: ChatMemoryModel
# ------------------------------
class ChatMemoryModel(Base):
    """
    Representa un mensaje almacenado en el historial de chat.
    """
    __tablename__ = "chat_memory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), nullable=False, index=True)
    role = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<ChatMemoryModel id={self.id} role={self.role} session={self.session_id}>"
