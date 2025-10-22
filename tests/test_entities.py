import pytest
from datetime import datetime
from src.domain.entities import Product, ChatMessage, ChatContext

# -------------------------------
# Test Product
# -------------------------------

def test_product_valid_data():
    product = Product(
        id=1,
        name="Camisa",
        brand="Nike",
        category="Ropa",
        size="M",
        color="Rojo",
        price=49.99,
        stock=10,
        description="Camisa deportiva de algodón"
    )
    assert product.is_available() is True
    assert product.price == 49.99

def test_product_reduce_stock():
    product = Product(
        id=1,
        name="Camisa",
        brand="Nike",
        category="Ropa",
        size="M",
        color="Rojo",
        price=49.99,
        stock=5,
        description="Camisa deportiva"
    )
    product.reduce_stock(2)
    assert product.stock == 3

def test_product_reduce_stock_insufficient():
    product = Product(
        id=1,
        name="Zapatos",
        brand="Adidas",
        category="Calzado",
        size="42",
        color="Negro",
        price=100,
        stock=1,
        description="Zapatillas running"
    )
    with pytest.raises(ValueError, match="Stock insuficiente"):
        product.reduce_stock(2)

# -------------------------------
# Test ChatMessage
# -------------------------------

def test_chat_message_valid():
    msg = ChatMessage(
        id=1,
        session_id="123",
        role="user",
        message="Hola",
        timestamp=datetime.utcnow()
    )
    assert msg.role == "user"
    assert isinstance(msg.timestamp, datetime)

# -------------------------------
# Test ChatContext
# -------------------------------

def test_chat_context_format_for_prompt():
    msgs = [
        ChatMessage(id=1, session_id="x", role="user", message="Hola", timestamp=datetime.utcnow()),
        ChatMessage(id=2, session_id="x", role="assistant", message="¡Hola! ¿En qué puedo ayudarte?", timestamp=datetime.utcnow())
    ]
    ctx = ChatContext(messages=msgs)
    formatted = ctx.format_for_prompt()
    assert "Hola" in formatted
    assert "assistant" in formatted
