from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class Cliente(Base):
    __tablename__ = "cliente"

    idcliente = Column(Integer, primary_key=True, index=True)
    tipodocumento = Column(String(30), nullable=False)
    numdocumento = Column(String(30), nullable=False)
    nombres = Column(String(60), nullable=False)
    apellidos = Column(String(60), nullable=False)
    telefono = Column(String(20))
    correo = Column(String(100))
    direccion = Column(String(150))

    expedientes = relationship(
    "Expediente",
    back_populates="cliente"
    )
    