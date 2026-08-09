from pydantic import BaseModel


class ClienteBase(BaseModel):
    tipodocumento: str
    numdocumento: str
    nombres: str
    apellidos: str
    telefono: str | None = None
    correo: str | None = None
    direccion: str | None = None


class ClienteCreate(ClienteBase):
    pass


class ClienteResponse(ClienteBase):
    idcliente: int

    class Config:
        from_attributes = True