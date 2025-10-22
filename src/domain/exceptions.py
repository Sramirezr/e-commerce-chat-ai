"""
Excepciones específicas del dominio.
Representan errores de negocio, no errores técnicos.
"""


class ProductNotFoundError(Exception):
    """
    Se lanza cuando se busca un producto que no existe.

    Attributes:
        message (str): Mensaje de error descriptivo.
    """

    def __init__(self, product_id: int = None):
        """
        Constructor de la excepción.

        Args:
            product_id (int, optional): ID del producto que no fue encontrado.

        Example:
            >>> raise ProductNotFoundError(10)
            ProductNotFoundError: Producto con ID 10 no encontrado
        """
        if product_id:
            self.message = f"Producto con ID {product_id} no encontrado"
        else:
            self.message = "Producto no encontrado"
        super().__init__(self.message)


class InvalidProductDataError(Exception):
    """
    Se lanza cuando los datos de un producto son inválidos.

    Attributes:
        message (str): Mensaje de error descriptivo.
    """

    def __init__(self, message: str = "Datos de producto inválidos"):
        """
        Constructor de la excepción.

        Args:
            message (str): Mensaje personalizado del error.

        Example:
            >>> raise InvalidProductDataError("Precio debe ser positivo")
        """
        self.message = message
        super().__init__(self.message)


class ChatServiceError(Exception):
    """
    Se lanza cuando ocurre un error en el servicio de chat.

    Attributes:
        message (str): Mensaje de error descriptivo.
    """

    def __init__(self, message: str = "Error en el servicio de chat"):
        """
        Constructor de la excepción.

        Args:
            message (str): Mensaje personalizado del error.

        Example:
            >>> raise ChatServiceError("Falla al conectarse con Gemini API")
        """
        self.message = message
        super().__init__(self.message)
