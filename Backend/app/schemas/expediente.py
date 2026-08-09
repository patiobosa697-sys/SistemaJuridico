from pydantic import BaseModel
from datetime import date


class ExpedienteBase(BaseModel):
    codigointerno: str | None = None
    numeroradicado: str | None = None
    asunto: str | None = None
    descripcion: str | None = None
    estado: str | None = None
    fechaapertura: date | None = None
    fechacierre: date | None = None
    idcliente: int
    idespecialidad: int


class ExpedienteCreate(ExpedienteBase):
    pass


class ExpedienteResponse(ExpedienteBase):
    idexpediente: int

    class Config:
        from_attributes = True