from pydantic import BaseModel


class UsuarioBase(BaseModel):
    nombres: str
    apellidos: str
    correo: str
    telefono: str | None = None
    estadoactual: str | None = None
    idrol: int


class UsuarioCreate(UsuarioBase):
    contrasenia: str


class UsuarioResponse(UsuarioBase):
    idusuario: int

    class Config:
        from_attributes = True