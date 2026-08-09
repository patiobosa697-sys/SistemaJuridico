from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship


class Rol(Base):
    __tablename__ = "rol"

    idrol = Column(Integer, primary_key=True, index=True)
    nombrerol = Column(String(30), nullable=False)
    usuarios = relationship(
    "Usuario",
    back_populates="rol"
)