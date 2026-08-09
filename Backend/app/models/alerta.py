from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Alerta(Base):
    __tablename__ = "alerta"

    idalerta = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    descripcion = Column(Text)
    fechaprogramada = Column(DateTime)
    estado = Column(String(30))

    idexpediente = Column(
        Integer,
        ForeignKey("expediente.idexpediente")
    )

    expediente = relationship(
    "Expediente",
    back_populates="alertas"
    )