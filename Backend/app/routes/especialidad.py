from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.especialidad import Especialidad
from app.schemas.especialidad import EspecialidadCreate, EspecialidadResponse
import traceback


router = APIRouter(
    prefix="/especialidades",
    tags=["Especialidades"]
)


@router.get("/", response_model=list[EspecialidadResponse])
def listar_especialidades():
    db: Session = SessionLocal()

    try:
        return db.query(Especialidad).all()

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.get("/{idespecialidad}", response_model=EspecialidadResponse)
def obtener_especialidad(idespecialidad: int):
    db: Session = SessionLocal()

    try:
        especialidad = db.query(Especialidad).filter(
            Especialidad.idespecialidad == idespecialidad
        ).first()

        if not especialidad:
            raise HTTPException(
                status_code=404,
                detail="Especialidad no encontrada"
            )

        return especialidad

    except HTTPException:
        raise

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.post("/", response_model=EspecialidadResponse, status_code=201)
def crear_especialidad(especialidad: EspecialidadCreate):
    db: Session = SessionLocal()

    try:
        nueva_especialidad = Especialidad(
            nombreesp=especialidad.nombreesp,
            descripcion=especialidad.descripcion
        )

        db.add(nueva_especialidad)
        db.commit()
        db.refresh(nueva_especialidad)

        return nueva_especialidad

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.put("/{idespecialidad}", response_model=EspecialidadResponse)
def actualizar_especialidad(
    idespecialidad: int,
    datos: EspecialidadCreate
):
    db: Session = SessionLocal()

    try:
        especialidad = db.query(Especialidad).filter(
            Especialidad.idespecialidad == idespecialidad
        ).first()

        if not especialidad:
            raise HTTPException(
                status_code=404,
                detail="Especialidad no encontrada"
            )

        especialidad.nombreesp = datos.nombreesp
        especialidad.descripcion = datos.descripcion

        db.commit()
        db.refresh(especialidad)

        return especialidad

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.delete("/{idespecialidad}")
def eliminar_especialidad(idespecialidad: int):
    db: Session = SessionLocal()

    try:
        especialidad = db.query(Especialidad).filter(
            Especialidad.idespecialidad == idespecialidad
        ).first()

        if not especialidad:
            raise HTTPException(
                status_code=404,
                detail="Especialidad no encontrada"
            )

        db.delete(especialidad)
        db.commit()

        return {
            "mensaje": "Especialidad eliminada correctamente"
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()