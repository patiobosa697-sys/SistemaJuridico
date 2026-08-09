from pydantic import BaseModel
from datetime import date


class DocumentoBase(BaseModel):
    nombre: str
    tipodocumento: str
    rutaarchivo: str | None = None
    fechasubida: date | None = None
    descripcion: str | None = None
    idexpediente: int


class DocumentoCreate(DocumentoBase):
    pass


class DocumentoResponse(DocumentoBase):
    iddocumento: int

    class Config:
        from_attributes = True