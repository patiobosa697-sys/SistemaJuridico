from sqlalchemy import Column, Integer, String

from app.database import Base
from sqlalchemy.orm import relationship


class Especialidad(Base):
    __tablename__ = "especialidad"

    idespecialidad = Column(Integer, primary_key=True, index=True)
    nombreesp = Column(String(60), nullable=False)
    descripcion = Column(String(255))
    expedientes = relationship(
    "Expediente",
    back_populates="especialidad"
    )

    usuarios = relationship(
    "UsuarioEspecialidad",
    back_populates="especialidad"
    )

