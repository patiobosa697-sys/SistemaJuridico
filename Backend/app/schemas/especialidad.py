from pydantic import BaseModel


class EspecialidadBase(BaseModel):
    nombreesp: str
    descripcion: str | None = None


class EspecialidadCreate(EspecialidadBase):
    pass


class EspecialidadResponse(EspecialidadBase):
    idespecialidad: int

    class Config:
        from_attributes = True