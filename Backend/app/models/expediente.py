from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Expediente(Base):
    __tablename__ = "expediente"

    idexpediente = Column(Integer, primary_key=True, index=True)
    codigointerno = Column(String(50))
    numeroradicado = Column(String(50))
    asunto = Column(String(100))
    descripcion = Column(String(255))
    estado = Column(String(30))
    fechaapertura = Column(Date)
    fechacierre = Column(Date)

    idcliente = Column(Integer, ForeignKey("cliente.idcliente"))
    idespecialidad = Column(Integer, ForeignKey("especialidad.idespecialidad"))

    cliente = relationship(
        "Cliente",
        back_populates="expedientes"
    )

    especialidad = relationship(
        "Especialidad",
        back_populates="expedientes"
    )

    documentos = relationship(
        "Documento",
        back_populates="expediente"
    )

    actuaciones = relationship(
        "Actuacion",
        back_populates="expediente"
    )

    audiencias = relationship(
        "Audiencia",
        back_populates="expediente"
    )

    alertas = relationship(
        "Alerta",
        back_populates="expediente"
    )

    usuarios_asignados = relationship(
        "ExpedienteUsuario",
        back_populates="expediente"
    )

