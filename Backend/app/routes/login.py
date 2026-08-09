from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.usuario import Usuario
from app.schemas.login import LoginRequest, LoginResponse
import traceback


router = APIRouter(
    prefix="/login",
    tags=["Autenticación"]
)


@router.post("/", response_model=LoginResponse)
def iniciar_sesion(datos: LoginRequest):
    db: Session = SessionLocal()

    try:
        usuario = db.query(Usuario).filter(
            Usuario.correo == datos.correo
        ).first()

        if not usuario:
            raise HTTPException(
                status_code=401,
                detail="Correo o contraseña incorrectos"
            )

        if usuario.contrasenia != datos.contrasenia:
            raise HTTPException(
                status_code=401,
                detail="Correo o contraseña incorrectos"
            )

        return {
            "mensaje": "Inicio de sesión exitoso",
            "idusuario": usuario.idusuario,
            "nombres": usuario.nombres,
            "apellidos": usuario.apellidos,
            "idrol": usuario.idrol
        }

    except HTTPException:
        raise

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        db.close()