from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)

# URL de conexión a PostgreSQL
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Crear el motor de conexión
engine = create_engine(DATABASE_URL)

# Crear sesiones para la base de datos
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.rol import Rol
from app.models.usuario import Usuario
from app.models.especialidad import Especialidad
from app.models.cliente import Cliente
from app.models.expediente import Expediente
from app.models.documento import Documento
from app.models.actuacion import Actuacion
from app.models.audiencia import Audiencia
from app.models.alerta import Alerta
from app.models.usuario_especialidad import UsuarioEspecialidad
from app.models.expediente_usuario import ExpedienteUsuario