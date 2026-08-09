from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class UsuarioEspecialidad(Base):
    __tablename__ = "usuario_especialidad"

    idusuario = Column(
        Integer,
        ForeignKey("usuario.idusuario"),
        primary_key=True
    )

    idespecialidad = Column(
        Integer,
        ForeignKey("especialidad.idespecialidad"),
        primary_key=True
    )

    usuario = relationship(
    "Usuario",
    back_populates="especialidades"
    )

    especialidad = relationship(
    "Especialidad",
    back_populates="usuarios"
    )