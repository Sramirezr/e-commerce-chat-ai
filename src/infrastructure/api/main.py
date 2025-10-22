from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from src.infrastructure.db.database import init_db, get_db
from src.infrastructure.repositories.product_repository import SQLProductRepository
from src.infrastructure.repositories.chat_repository import SQLChatRepository
from src.application.product_service import ProductService
from src.application.chat_service import ChatService
from src.application.dtos import ProductDTO, ChatMessageRequestDTO, ChatMessageResponseDTO, ChatHistoryDTO
from src.infrastructure.llm_providers.gemini_service import GeminiService

# ------------------------------------------------------------
# Inicialización de FastAPI
# ------------------------------------------------------------
app = FastAPI(
    title="E-Commerce Chat AI API",
    description="API de chat inteligente para e-commerce de zapatos (Undercore Project)",
    version="1.0.0",
)

# ------------------------------------------------------------
# Configurar CORS
# ------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, limita esto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------
# Evento de inicio - Inicializa la base de datos
# ------------------------------------------------------------
@app.on_event("startup")
def on_startup():
    init_db()


# ------------------------------------------------------------
# Endpoint raíz
# ------------------------------------------------------------
@app.get("/")
def root():
    """
    Información básica de la API.
    """
    return {
        "app": "E-Commerce Chat AI API",
        "version": "1.0.0",
        "description": "Asistente virtual de ventas impulsado por IA (Google Gemini).",
        "endpoints": [
            "/products",
            "/products/{id}",
            "/chat",
            "/chat/history/{session_id}",
            "/health",
        ],
    }


# ------------------------------------------------------------
# Obtener todos los productos
# ------------------------------------------------------------
@app.get("/products", response_model=List[ProductDTO])
def get_all_products(db: Session = Depends(get_db)):
    repo = SQLProductRepository(db)
    service = ProductService(repo)
    return service.get_all_products()


# ------------------------------------------------------------
# Obtener producto por ID
# ------------------------------------------------------------
@app.get("/products/{product_id}", response_model=ProductDTO)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    repo = SQLProductRepository(db)
    service = ProductService(repo)
    product = service.get_product_by_id(product_id)

    if not product:
        raise HTTPException(status_code=404, detail=f"Producto con ID {product_id} no encontrado")

    return product


# ------------------------------------------------------------
# Endpoint de Chat con IA
# ------------------------------------------------------------
@app.post("/chat", response_model=ChatMessageResponseDTO)
async def chat_with_ai(request: ChatMessageRequestDTO, db: Session = Depends(get_db)):
    """
    Procesa un mensaje del usuario, genera una respuesta de IA
    y guarda el historial de conversación.
    """
    try:
        # Repositorios y servicios
        product_repo = SQLProductRepository(db)
        chat_repo = SQLChatRepository(db)
        gemini_service = GeminiService()
        chat_service = ChatService(product_repo, chat_repo, gemini_service)

        # Generar respuesta con IA
        response = await chat_service.process_user_message(request)
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


# ------------------------------------------------------------
# Obtener historial de chat
# ------------------------------------------------------------
@app.get("/chat/history/{session_id}", response_model=List[ChatHistoryDTO])
def get_chat_history(
    session_id: str,
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Retorna los últimos N mensajes del historial de chat de una sesión.
    """
    repo = SQLChatRepository(db)
    service = ChatService(None, repo, None)
    return service.get_session_history(session_id, limit)


# ------------------------------------------------------------
# Eliminar historial de chat
# ------------------------------------------------------------
@app.delete("/chat/history/{session_id}")
def delete_chat_history(session_id: str, db: Session = Depends(get_db)):
    repo = SQLChatRepository(db)
    service = ChatService(None, repo, None)
    deleted_count = service.delete_session_history(session_id)
    return {"deleted": deleted_count}


# ------------------------------------------------------------
# Health Check
# ------------------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}
