from sqlalchemy import Column, Integer, String, Text, Date, Time, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Audiencia(Base):
    __tablename__ = "audiencia"

    idaudiencia = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date)
    hora = Column(Time)
    lugar = Column(String(150))
    juzgado = Column(String(150))
    estado = Column(String(30))
    observaciones = Column(Text)

    idexpediente = Column(
        Integer,
        ForeignKey("expediente.idexpediente")
    )

    expediente = relationship(
    "Expediente",
    back_populates="audiencias"
    )