from pydantic import BaseModel


class UsuarioEspecialidadBase(BaseModel):
    idusuario: int
    idespecialidad: int


class UsuarioEspecialidadCreate(UsuarioEspecialidadBase):
    pass


class UsuarioEspecialidadResponse(UsuarioEspecialidadBase):
    class Config:
        from_attributes = True