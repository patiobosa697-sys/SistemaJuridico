from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Actuacion(Base):
    __tablename__ = "actuacion"

    idactuacion = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50), nullable=False)
    descripcion = Column(Text)
    fecha = Column(Date)
    observaciones = Column(Text)

    idexpediente = Column(
        Integer,
        ForeignKey("expediente.idexpediente")
    )

    expediente = relationship(
    "Expediente",
    back_populates="actuaciones"
    )