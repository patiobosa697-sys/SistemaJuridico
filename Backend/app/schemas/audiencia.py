from pydantic import BaseModel
from datetime import date, time


class AudienciaBase(BaseModel):
    fecha: date
    hora: time
    lugar: str
    juzgado: str
    estado: str
    observaciones: str | None = None
    idexpediente: int


class AudienciaCreate(AudienciaBase):
    pass


class AudienciaResponse(AudienciaBase):
    idaudiencia: int

    class Config:
        from_attributes = True