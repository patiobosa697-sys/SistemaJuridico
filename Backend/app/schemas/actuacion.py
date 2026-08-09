from pydantic import BaseModel
from datetime import date


class ActuacionBase(BaseModel):
    tipo: str
    descripcion: str | None = None
    fecha: date | None = None
    observaciones: str | None = None
    idexpediente: int


class ActuacionCreate(ActuacionBase):
    pass


class ActuacionResponse(ActuacionBase):
    idactuacion: int

    class Config:
        from_attributes = True