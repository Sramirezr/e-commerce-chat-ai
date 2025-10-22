from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Product, ChatMessage


# ---------------------------------------------
# Interface: IProductRepository
# ---------------------------------------------
class IProductRepository(ABC):
    """
    Interface que define el contrato para acceder a productos.
    Las implementaciones concretas estarán en la capa de infraestructura.
    """

    @abstractmethod
    def get_all(self) -> List[Product]:
        """
        Obtiene todos los productos registrados.

        Returns:
            List[Product]: Lista de todos los productos.
        """
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Obtiene un producto por su ID.

        Args:
            product_id (int): Identificador del producto.

        Returns:
            Optional[Product]: El producto encontrado o None si no existe.
        """
        pass

    @abstractmethod
    def get_by_brand(self, brand: str) -> List[Product]:
        """
        Obtiene todos los productos de una marca específica.

        Args:
            brand (str): Nombre de la marca.

        Returns:
            List[Product]: Lista de productos de esa marca.
        """
        pass

    @abstractmethod
    def get_by_category(self, category: str) -> List[Product]:
        """
        Obtiene productos de una categoría específica.

        Args:
            category (str): Categoría (e.g., Running, Casual, Formal).

        Returns:
            List[Product]: Lista de productos de esa categoría.
        """
        pass

    @abstractmethod
    def save(self, product: Product) -> Product:
        """
        Guarda o actualiza un producto en la base de datos.

        Args:
            product (Product): Entidad del producto a guardar.

        Returns:
            Product: El producto guardado (con ID asignado si es nuevo).
        """
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """
        Elimina un producto por su ID.

        Args:
            product_id (int): Identificador del producto.

        Returns:
            bool: True si se eliminó, False si no existía.
        """
        pass


# ---------------------------------------------
# Interface: IChatRepository
# ---------------------------------------------
class IChatRepository(ABC):
    """
    Interface para gestionar el historial de conversaciones del chat.
    """

    @abstractmethod
    def save_message(self, message: ChatMessage) -> ChatMessage:
        """
        Guarda un mensaje en el historial del chat.

        Args:
            message (ChatMessage): Entidad de mensaje.

        Returns:
            ChatMessage: El mensaje guardado con ID asignado.
        """
        pass

    @abstractmethod
    def get_session_history(self, session_id: str, limit: Optional[int] = None) -> List[ChatMessage]:
        """
        Obtiene el historial completo de una sesión específica.

        Args:
            session_id (str): Identificador único de la sesión.
            limit (Optional[int]): Límite de cantidad de mensajes a recuperar.

        Returns:
            List[ChatMessage]: Lista de mensajes ordenados cronológicamente.
        """
        pass

    @abstractmethod
    def delete_session_history(self, session_id: str) -> int:
        """
        Elimina todo el historial de una sesión.

        Args:
            session_id (str): Identificador de la sesión.

        Returns:
            int: Cantidad de mensajes eliminados.
        """
        pass

    @abstractmethod
    def get_recent_messages(self, session_id: str, count: int) -> List[ChatMessage]:
        """
        Obtiene los últimos N mensajes de una sesión (orden cronológico).

        Args:
            session_id (str): Identificador de la sesión.
            count (int): Cantidad máxima de mensajes a recuperar.

        Returns:
            List[ChatMessage]: Lista de mensajes recientes.
        """
        pass
