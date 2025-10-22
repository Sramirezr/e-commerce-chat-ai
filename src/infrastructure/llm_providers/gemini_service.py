import os
import google.generativeai as genai
from dotenv import load_dotenv
from src.domain.entities import ChatContext

# Cargar variables de entorno desde .env
load_dotenv()


class GeminiService:
    """
    Servicio para interactuar con el modelo de Google Gemini.
    Integra IA conversacional con información del e-commerce.
    """

    def __init__(self):
        # Cargar API key desde variables de entorno
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("❌ GEMINI_API_KEY no encontrada en el entorno (.env)")

        # Configurar cliente de Gemini
        genai.configure(api_key=self.api_key)

        # Inicializar modelo (versión rápida y rentable)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    async def generate_response(self, user_message: str, products: list, context: ChatContext) -> str:
        """
        Genera una respuesta de Gemini combinando productos, contexto y mensaje actual.
        """

        # 1️⃣ Formatear productos
        products_info = self.format_products_info(products)

        # 2️⃣ Formatear contexto conversacional
        context_text = context.format_for_prompt() if context else ""

        # 3️⃣ Construir prompt completo
        prompt = f"""
Eres un asistente virtual experto en ventas de zapatos para un e-commerce.
Tu objetivo es ayudar a los clientes a encontrar los zapatos perfectos.

PRODUCTOS DISPONIBLES:
{products_info}

INSTRUCCIONES:
- Sé amigable y profesional
- Usa el contexto de la conversación anterior
- Recomienda productos específicos cuando sea apropiado
- Menciona precios, tallas y disponibilidad
- Si no tienes información, sé honesto

HISTORIAL DE CONVERSACIÓN:
{context_text}

Usuario: {user_message}

Asistente:
"""

        # 4️⃣ Llamar a Gemini API
        try:
            response = await self.model.generate_content_async(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"⚠️ Error al generar respuesta con Gemini: {e}")
            return "Lo siento, hubo un problema al procesar tu mensaje. Inténtalo nuevamente más tarde."

    def format_products_info(self, products: list) -> str:
        """
        Convierte una lista de productos a texto legible.
        Ejemplo:
        - Nike Air Zoom | Nike | $120 | Stock: 8
        """
        if not products:
            return "No hay productos disponibles en este momento."

        formatted = []
        for p in products:
            formatted.append(
                f"- {p.name} | {p.brand} | ${p.price:.2f} | Talla: {p.size} | Stock: {p.stock}"
            )
        return "\n".join(formatted)
