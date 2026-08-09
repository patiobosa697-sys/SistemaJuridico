from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.expediente_usuario import ExpedienteUsuario
from app.schemas.expediente_usuario import (
    ExpedienteUsuarioCreate,
    ExpedienteUsuarioResponse
)
import traceback


router = APIRouter(
    prefix="/expedientes-usuarios",
    tags=["Expediente Usuario"]
)


@router.get("/", response_model=list[ExpedienteUsuarioResponse])
def listar_asignaciones():
    db: Session = SessionLocal()

    try:
        return db.query(ExpedienteUsuario).all()

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.post(
    "/",
    response_model=ExpedienteUsuarioResponse,
    status_code=201
)
def crear_asignacion(datos: ExpedienteUsuarioCreate):
    db: Session = SessionLocal()

    try:
        existe = db.query(ExpedienteUsuario).filter(
            ExpedienteUsuario.idexpediente == datos.idexpediente,
            ExpedienteUsuario.idusuario == datos.idusuario
        ).first()

        if existe:
            raise HTTPException(
                status_code=400,
                detail="El usuario ya está asignado a este expediente"
            )

        nueva_asignacion = ExpedienteUsuario(
            idexpediente=datos.idexpediente,
            idusuario=datos.idusuario,
            responsable=datos.responsable,
            fechaasignacion=datos.fechaasignacion
        )

        db.add(nueva_asignacion)
        db.commit()
        db.refresh(nueva_asignacion)

        return nueva_asignacion

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.delete("/")
def eliminar_asignacion(
    idexpediente: int,
    idusuario: int
):
    db: Session = SessionLocal()

    try:
        asignacion = db.query(ExpedienteUsuario).filter(
            ExpedienteUsuario.idexpediente == idexpediente,
            ExpedienteUsuario.idusuario == idusuario
        ).first()

        if not asignacion:
            raise HTTPException(
                status_code=404,
                detail="Asignación no encontrada"
            )

        db.delete(asignacion)
        db.commit()

        return {
            "mensaje": "Asignación eliminada correctamente"
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()