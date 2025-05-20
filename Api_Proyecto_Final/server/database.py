from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
# Load environment variables from .env file
load_dotenv()
# Obtener la URL de la base de datos desde las variables de entorno
# Get database URL from environment variables
SQL_ALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Crear el motor de SQLAlchemy
# Create SQLAlchemy engine
engine = create_engine(
    SQL_ALCHEMY_DATABASE_URL
)
# Crear una fábrica de sesiones locales
# Create a local session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Clase base declarativa para los modelos
# Declarative base class for models
Base = declarative_base()
