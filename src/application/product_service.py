from src.application.dtos import ProductDTO
from src.domain.repositories import IProductRepository


class ProductService:
    """
    Servicio de aplicación para manejar la lógica de productos.
    """

    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository

    def get_all_products(self):
        """
        Retorna todos los productos disponibles.
        """
        products = self.product_repository.get_all()
        return [ProductDTO.from_entity(p) for p in products]

    def get_product_by_id(self, product_id: int):
        """
        Retorna un producto específico por ID.
        """
        product = self.product_repository.get_by_id(product_id)
        return ProductDTO.from_entity(product) if product else None
