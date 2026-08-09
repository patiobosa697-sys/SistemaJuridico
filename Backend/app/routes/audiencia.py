from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.audiencia import Audiencia
from app.schemas.audiencia import AudienciaCreate, AudienciaResponse
import traceback


router = APIRouter(
    prefix="/audiencias",
    tags=["Audiencias"]
)


@router.get("/", response_model=list[AudienciaResponse])
def listar_audiencias():
    db: Session = SessionLocal()

    try:
        return db.query(Audiencia).all()

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.get("/{idaudiencia}", response_model=AudienciaResponse)
def obtener_audiencia(idaudiencia: int):
    db: Session = SessionLocal()

    try:
        audiencia = db.query(Audiencia).filter(
            Audiencia.idaudiencia == idaudiencia
        ).first()

        if not audiencia:
            raise HTTPException(
                status_code=404,
                detail="Audiencia no encontrada"
            )

        return audiencia

    except HTTPException:
        raise

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.post("/", response_model=AudienciaResponse, status_code=201)
def crear_audiencia(datos: AudienciaCreate):
    db: Session = SessionLocal()

    try:
        nueva_audiencia = Audiencia(
            fecha=datos.fecha,
            hora=datos.hora,
            lugar=datos.lugar,
            juzgado=datos.juzgado,
            estado=datos.estado,
            observaciones=datos.observaciones,
            idexpediente=datos.idexpediente
        )

        db.add(nueva_audiencia)
        db.commit()
        db.refresh(nueva_audiencia)

        return nueva_audiencia

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.put("/{idaudiencia}", response_model=AudienciaResponse)
def actualizar_audiencia(
    idaudiencia: int,
    datos: AudienciaCreate
):
    db: Session = SessionLocal()

    try:
        audiencia = db.query(Audiencia).filter(
            Audiencia.idaudiencia == idaudiencia
        ).first()

        if not audiencia:
            raise HTTPException(
                status_code=404,
                detail="Audiencia no encontrada"
            )

        audiencia.fecha = datos.fecha
        audiencia.hora = datos.hora
        audiencia.lugar = datos.lugar
        audiencia.juzgado = datos.juzgado
        audiencia.estado = datos.estado
        audiencia.observaciones = datos.observaciones
        audiencia.idexpediente = datos.idexpediente

        db.commit()
        db.refresh(audiencia)

        return audiencia

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.delete("/{idaudiencia}")
def eliminar_audiencia(idaudiencia: int):
    db: Session = SessionLocal()

    try:
        audiencia = db.query(Audiencia).filter(
            Audiencia.idaudiencia == idaudiencia
        ).first()

        if not audiencia:
            raise HTTPException(
                status_code=404,
                detail="Audiencia no encontrada"
            )

        db.delete(audiencia)
        db.commit()

        return {
            "mensaje": "Audiencia eliminada correctamente"
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()