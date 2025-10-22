from src.domain.repositories import IProductRepository, IChatRepository
from src.infrastructure.llm_providers.gemini_service import GeminiService
from src.application.dtos import ChatMessageRequestDTO, ChatMessageResponseDTO, ChatHistoryDTO
from src.domain.entities import ChatMessage, ChatContext
from datetime import datetime


class ChatService:
    """
    Servicio de aplicación que integra IA + historial de conversación.
    """

    def __init__(self, product_repo: IProductRepository, chat_repo: IChatRepository, gemini_service: GeminiService):
        self.product_repo = product_repo
        self.chat_repo = chat_repo
        self.gemini_service = gemini_service

    async def process_user_message(self, request: ChatMessageRequestDTO):
        """
        Procesa un mensaje del usuario, genera una respuesta y guarda ambos mensajes.
        """

        # 1️⃣ Guardar mensaje del usuario
        user_msg = ChatMessage(
            id=None,
            session_id=request.session_id,
            role="user",
            message=request.message,
            timestamp=datetime.utcnow()
        )
        self.chat_repo.save_message(user_msg)

        # 2️⃣ Recuperar historial reciente
        recent_msgs = self.chat_repo.get_recent_messages(request.session_id, limit=6)
        context = ChatContext(messages=recent_msgs)

        # 3️⃣ Obtener productos disponibles
        products = self.product_repo.get_all()

        # 4️⃣ Generar respuesta con Gemini
        response_text = await self.gemini_service.generate_response(request.message, products, context)

        # 5️⃣ Guardar mensaje del asistente
        assistant_msg = ChatMessage(
            id=None,
            session_id=request.session_id,
            role="assistant",
            message=response_text,
            timestamp=datetime.utcnow()
        )
        self.chat_repo.save_message(assistant_msg)

        # 6️⃣ Retornar DTO de respuesta
        return ChatMessageResponseDTO(session_id=request.session_id, response=response_text)

    def get_session_history(self, session_id: str, limit: int = 10):
        """
        Obtiene el historial de chat de una sesión.
        """
        messages = self.chat_repo.get_session_history(session_id, limit)
        return [ChatHistoryDTO.from_entity(m) for m in messages]

    def delete_session_history(self, session_id: str):
        """
        Elimina el historial de chat por session_id.
        """
        return self.chat_repo.delete_session_history(session_id)
