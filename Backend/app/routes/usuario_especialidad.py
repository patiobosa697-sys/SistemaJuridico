from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.usuario_especialidad import UsuarioEspecialidad
from app.schemas.usuario_especialidad import (
    UsuarioEspecialidadCreate,
    UsuarioEspecialidadResponse
)
import traceback


router = APIRouter(
    prefix="/usuarios-especialidades",
    tags=["Usuario Especialidad"]
)


@router.get("/", response_model=list[UsuarioEspecialidadResponse])
def listar_asignaciones():
    db: Session = SessionLocal()

    try:
        return db.query(UsuarioEspecialidad).all()

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.post(
    "/",
    response_model=UsuarioEspecialidadResponse,
    status_code=201
)
def crear_asignacion(datos: UsuarioEspecialidadCreate):
    db: Session = SessionLocal()

    try:
        existe = db.query(UsuarioEspecialidad).filter(
            UsuarioEspecialidad.idusuario == datos.idusuario,
            UsuarioEspecialidad.idespecialidad == datos.idespecialidad
        ).first()

        if existe:
            raise HTTPException(
                status_code=400,
                detail="El usuario ya está asignado a esta especialidad"
            )

        nueva_asignacion = UsuarioEspecialidad(
            idusuario=datos.idusuario,
            idespecialidad=datos.idespecialidad
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
    idusuario: int,
    idespecialidad: int
):
    db: Session = SessionLocal()

    try:
        asignacion = db.query(UsuarioEspecialidad).filter(
            UsuarioEspecialidad.idusuario == idusuario,
            UsuarioEspecialidad.idespecialidad == idespecialidad
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