from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.actuacion import Actuacion
from app.schemas.actuacion import ActuacionCreate, ActuacionResponse
import traceback


router = APIRouter(
    prefix="/actuaciones",
    tags=["Actuaciones"]
)


@router.get("/", response_model=list[ActuacionResponse])
def listar_actuaciones():
    db: Session = SessionLocal()

    try:
        return db.query(Actuacion).all()

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.get("/{idactuacion}", response_model=ActuacionResponse)
def obtener_actuacion(idactuacion: int):
    db: Session = SessionLocal()

    try:
        actuacion = db.query(Actuacion).filter(
            Actuacion.idactuacion == idactuacion
        ).first()

        if not actuacion:
            raise HTTPException(
                status_code=404,
                detail="Actuación no encontrada"
            )

        return actuacion

    except HTTPException:
        raise

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.post("/", response_model=ActuacionResponse, status_code=201)
def crear_actuacion(datos: ActuacionCreate):
    db: Session = SessionLocal()

    try:
        nueva_actuacion = Actuacion(
            tipo=datos.tipo,
            descripcion=datos.descripcion,
            fecha=datos.fecha,
            observaciones=datos.observaciones,
            idexpediente=datos.idexpediente
        )

        db.add(nueva_actuacion)
        db.commit()
        db.refresh(nueva_actuacion)

        return nueva_actuacion

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.put("/{idactuacion}", response_model=ActuacionResponse)
def actualizar_actuacion(
    idactuacion: int,
    datos: ActuacionCreate
):
    db: Session = SessionLocal()

    try:
        actuacion = db.query(Actuacion).filter(
            Actuacion.idactuacion == idactuacion
        ).first()

        if not actuacion:
            raise HTTPException(
                status_code=404,
                detail="Actuación no encontrada"
            )

        actuacion.tipo = datos.tipo
        actuacion.descripcion = datos.descripcion
        actuacion.fecha = datos.fecha
        actuacion.observaciones = datos.observaciones
        actuacion.idexpediente = datos.idexpediente

        db.commit()
        db.refresh(actuacion)

        return actuacion

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.delete("/{idactuacion}")
def eliminar_actuacion(idactuacion: int):
    db: Session = SessionLocal()

    try:
        actuacion = db.query(Actuacion).filter(
            Actuacion.idactuacion == idactuacion
        ).first()

        if not actuacion:
            raise HTTPException(
                status_code=404,
                detail="Actuación no encontrada"
            )

        db.delete(actuacion)
        db.commit()

        return {
            "mensaje": "Actuación eliminada correctamente"
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()