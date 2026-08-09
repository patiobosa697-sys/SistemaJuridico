from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Documento(Base):
    __tablename__ = "documento"

    iddocumento = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    tipodocumento = Column(String(50))
    rutaarchivo = Column(String(255))
    fechasubida = Column(Date)
    descripcion = Column(String(255))

    idexpediente = Column(Integer, ForeignKey("expediente.idexpediente"))

    expediente = relationship(
    "Expediente",
    back_populates="documentos"
    )