from pydantic import BaseModel

class RolBase(BaseModel):
    nombrerol: str


class RolCreate(RolBase):
    pass


class RolResponse(RolBase):
    idrol: int

    class Config:
        from_attributes = True