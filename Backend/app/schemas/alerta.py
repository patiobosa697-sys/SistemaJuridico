from pydantic import BaseModel
from datetime import datetime


class AlertaBase(BaseModel):
    titulo: str
    descripcion: str | None = None
    fechaprogramada: datetime | None = None
    estado: str
    idexpediente: int


class AlertaCreate(AlertaBase):
    pass


class AlertaResponse(AlertaBase):
    idalerta: int

    class Config:
        from_attributes = True