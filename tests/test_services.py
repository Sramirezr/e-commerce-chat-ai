import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime
from src.application.chat_service import ChatService
from src.application.product_service import ProductService
from src.domain.entities import ChatMessage, Product
from src.application.dtos import ChatMessageRequestDTO


# -------------------------------
# Fixtures
# -------------------------------
@pytest.fixture
def mock_product_repo():
    repo = Mock()
    repo.get_all.return_value = [
        Product(id=1, name="Camisa", brand="Nike", category="Ropa",
                size="M", color="Rojo", price=49.99, stock=5,
                description="Camisa deportiva")
    ]
    return repo


@pytest.fixture
def mock_chat_repo():
    repo = Mock()
    repo.get_recent_messages.return_value = []
    repo.save_message.return_value = ChatMessage(
        id=1, session_id="x", role="user", message="Hola", timestamp=datetime.utcnow()
    )
    return repo


@pytest.fixture
def mock_gemini_service():
    service = AsyncMock()
    service.generate_response.return_value = "Te recomiendo la camisa roja Nike."
    return service


# -------------------------------
# ProductService
# -------------------------------
def test_get_all_products(mock_product_repo):
    service = ProductService(mock_product_repo)
    products = service.get_all_products()
    assert len(products) == 1
    assert products[0].name == "Camisa"


# -------------------------------
# ChatService (async)
# -------------------------------
@pytest.mark.asyncio
async def test_process_user_message(mock_product_repo, mock_chat_repo, mock_gemini_service):
    service = ChatService(mock_product_repo, mock_chat_repo, mock_gemini_service)
    dto = ChatMessageRequestDTO(session_id="test1", message="¿Qué me recomiendas?")
    result = await service.process_user_message(dto)
    assert "recomiendo" in result.response
    mock_chat_repo.save_message.assert_called()


@pytest.mark.asyncio
async def test_process_user_message_error(mock_product_repo, mock_chat_repo, mock_gemini_service):
    mock_gemini_service.generate_response.side_effect = Exception("Error IA")
    service = ChatService(mock_product_repo, mock_chat_repo, mock_gemini_service)
    dto = ChatMessageRequestDTO(session_id="test2", message="Hola")
    with pytest.raises(Exception):
        await service.process_user_message(dto)
