from src.domain.repositories import IChatRepository
from src.domain.entities import ChatMessage
from src.infrastructure.db.models import ChatMemoryModel
from datetime import datetime


class SQLChatRepository(IChatRepository):
    """
    Implementación SQLAlchemy del repositorio de mensajes del chat.
    """

    def __init__(self, db):
        self.db = db

    def save_message(self, message: ChatMessage):
        model = self._entity_to_model(message)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)

    def get_session_history(self, session_id: str, limit: int = 10):
        messages = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .order_by(ChatMemoryModel.timestamp.desc())
            .limit(limit)
            .all()
        )
        messages.reverse()
        return [self._model_to_entity(m) for m in messages]

    def delete_session_history(self, session_id: str):
        deleted = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .delete()
        )
        self.db.commit()
        return deleted

    def get_recent_messages(self, session_id: str, limit: int = 6):
        return self.get_session_history(session_id, limit)

    # -------------------------------------------------
    # Conversión ORM <-> Entidad
    # -------------------------------------------------
    def _model_to_entity(self, model: ChatMemoryModel):
        return ChatMessage(
            id=model.id,
            session_id=model.session_id,
            role=model.role,
            message=model.message,
            timestamp=model.timestamp,
        )

    def _entity_to_model(self, entity: ChatMessage):
        return ChatMemoryModel(
            id=entity.id,
            session_id=entity.session_id,
            role=entity.role,
            message=entity.message,
            timestamp=entity.timestamp or datetime.utcnow(),
        )
