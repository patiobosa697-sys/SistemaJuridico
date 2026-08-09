from pydantic import BaseModel


class LoginRequest(BaseModel):
    correo: str
    contrasenia: str


class LoginResponse(BaseModel):
    mensaje: str
    idusuario: int
    nombres: str
    apellidos: str
    idrol: int