from src.infrastructure.db.database import SessionLocal
from src.infrastructure.db.models import ProductModel


def load_initial_data():
    """
    Carga 10 productos de ejemplo si la base de datos está vacía.
    """
    db = SessionLocal()
    try:
        count = db.query(ProductModel).count()
        if count > 0:
            print("✅ Datos iniciales ya existen.")
            return

        products = [
            ProductModel(name="Nike Air Zoom Pegasus", brand="Nike", category="Running", size="42", color="Negro", price=150.0, stock=10, description="Zapatillas ligeras para correr."),
            ProductModel(name="Adidas Ultraboost", brand="Adidas", category="Running", size="43", color="Blanco", price=180.0, stock=8, description="Comodidad superior."),
            ProductModel(name="Puma Ignite", brand="Puma", category="Deportivo", size="41", color="Gris", price=120.0, stock=15, description="Estilo y rendimiento."),
            ProductModel(name="Reebok Classic", brand="Reebok", category="Casual", size="42", color="Blanco", price=90.0, stock=12, description="Un clásico urbano."),
            ProductModel(name="Converse Chuck Taylor", brand="Converse", category="Casual", size="40", color="Negro", price=70.0, stock=20, description="Ícono del calzado urbano."),
            ProductModel(name="Timberland Boot", brand="Timberland", category="Formal", size="44", color="Marrón", price=200.0, stock=5, description="Resistente y elegante."),
            ProductModel(name="Vans Old Skool", brand="Vans", category="Casual", size="41", color="Azul", price=85.0, stock=14, description="Estilo skate clásico."),
            ProductModel(name="New Balance 574", brand="New Balance", category="Running", size="42", color="Gris", price=110.0, stock=9, description="Confort y estilo."),
            ProductModel(name="Under Armour HOVR", brand="Under Armour", category="Running", size="43", color="Rojo", price=130.0, stock=7, description="Amortiguación avanzada."),
            ProductModel(name="Fila Disruptor II", brand="Fila", category="Casual", size="39", color="Blanco", price=95.0, stock=11, description="Diseño retro moderno."),
        ]

        db.add_all(products)
        db.commit()
        print("✅ Datos iniciales cargados correctamente.")

    except Exception as e:
        db.rollback()
        print(f"❌ Error al cargar datos: {e}")
    finally:
        db.close()
