from pydantic import BaseModel
from datetime import date


class ExpedienteUsuarioBase(BaseModel):
    idexpediente: int
    idusuario: int
    responsable: bool
    fechaasignacion: date | None = None


class ExpedienteUsuarioCreate(ExpedienteUsuarioBase):
    pass


class ExpedienteUsuarioResponse(ExpedienteUsuarioBase):
    class Config:
        from_attributes = True