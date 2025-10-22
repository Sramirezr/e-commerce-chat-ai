import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

# --------------------------------------------
# Crear carpeta 'data' si no existe
# --------------------------------------------
os.makedirs("data", exist_ok=True)

# --------------------------------------------
# URL de conexión a SQLite
# --------------------------------------------
DATABASE_URL = "sqlite:///./data/ecommerce_chat.db"

# --------------------------------------------
# Configuración del motor de base de datos
# --------------------------------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Creador de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para los modelos ORM
Base = declarative_base()


# --------------------------------------------
# Dependencia para obtener la sesión en FastAPI
# --------------------------------------------
def get_db():
    """
    Genera una sesión de base de datos para cada request de FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------------------------------
# Inicializador de la base de datos
# --------------------------------------------
def init_db():
    """
    Crea todas las tablas en la base de datos.
    """
    from src.infrastructure.db import models  # Import diferido
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas correctamente.")


# --------------------------------------------
# Ejecución directa del módulo
# --------------------------------------------
if __name__ == "__main__":
    init_db()
