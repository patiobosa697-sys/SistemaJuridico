from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    idusuario = Column(Integer, primary_key=True, index=True)
    nombres = Column(String(60), nullable=False)
    apellidos = Column(String(60), nullable=False)
    correo = Column(String(100), nullable=False)
    contrasenia = Column(String(255), nullable=False)
    telefono = Column(String(20))
    estadoactual = Column(String(20))

    idrol = Column(Integer, ForeignKey("rol.idrol"))

    rol = relationship(
    "Rol",
    back_populates="usuarios"
    )

    especialidades = relationship(
    "UsuarioEspecialidad",
    back_populates="usuario"
    )

    expedientes = relationship(
    "ExpedienteUsuario",
    back_populates="usuario"
    )