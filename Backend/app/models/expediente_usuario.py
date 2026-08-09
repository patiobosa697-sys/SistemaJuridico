from sqlalchemy import Column, Integer, Boolean, Date, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class ExpedienteUsuario(Base):
    __tablename__ = "expediente_usuario"

    idexpediente = Column(
        Integer,
        ForeignKey("expediente.idexpediente"),
        primary_key=True
    )

    idusuario = Column(
        Integer,
        ForeignKey("usuario.idusuario"),
        primary_key=True
    )

    responsable = Column(Boolean)
    fechaasignacion = Column(Date)

    usuario = relationship(
    "Usuario",
    back_populates="expedientes"
    )

    expediente = relationship(
    "Expediente",
    back_populates="usuarios_asignados"
    )