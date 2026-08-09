from dotenv import load_dotenv
from pathlib import Path
import os

# Cargar el archivo .env
ruta = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ruta)

# Variables de entorno
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Solo para comprobar que se cargaron (luego las quitaremos)
print("HOST:", DB_HOST)
print("PORT:", DB_PORT)
print("NAME:", DB_NAME)
print("USER:", DB_USER)