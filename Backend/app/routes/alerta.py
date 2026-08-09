from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.alerta import Alerta
from app.schemas.alerta import AlertaCreate, AlertaResponse
import traceback


router = APIRouter(
    prefix="/alertas",
    tags=["Alertas"]
)


@router.get("/", response_model=list[AlertaResponse])
def listar_alertas():
    db: Session = SessionLocal()

    try:
        return db.query(Alerta).all()

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.get("/{idalerta}", response_model=AlertaResponse)
def obtener_alerta(idalerta: int):
    db: Session = SessionLocal()

    try:
        alerta = db.query(Alerta).filter(
            Alerta.idalerta == idalerta
        ).first()

        if not alerta:
            raise HTTPException(
                status_code=404,
                detail="Alerta no encontrada"
            )

        return alerta

    except HTTPException:
        raise

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.post("/", response_model=AlertaResponse, status_code=201)
def crear_alerta(datos: AlertaCreate):
    db: Session = SessionLocal()

    try:
        nueva_alerta = Alerta(
            titulo=datos.titulo,
            descripcion=datos.descripcion,
            fechaprogramada=datos.fechaprogramada,
            estado=datos.estado,
            idexpediente=datos.idexpediente
        )

        db.add(nueva_alerta)
        db.commit()
        db.refresh(nueva_alerta)

        return nueva_alerta

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.put("/{idalerta}", response_model=AlertaResponse)
def actualizar_alerta(
    idalerta: int,
    datos: AlertaCreate
):
    db: Session = SessionLocal()

    try:
        alerta = db.query(Alerta).filter(
            Alerta.idalerta == idalerta
        ).first()

        if not alerta:
            raise HTTPException(
                status_code=404,
                detail="Alerta no encontrada"
            )

        alerta.titulo = datos.titulo
        alerta.descripcion = datos.descripcion
        alerta.fechaprogramada = datos.fechaprogramada
        alerta.estado = datos.estado
        alerta.idexpediente = datos.idexpediente

        db.commit()
        db.refresh(alerta)

        return alerta

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.delete("/{idalerta}")
def eliminar_alerta(idalerta: int):
    db: Session = SessionLocal()

    try:
        alerta = db.query(Alerta).filter(
            Alerta.idalerta == idalerta
        ).first()

        if not alerta:
            raise HTTPException(
                status_code=404,
                detail="Alerta no encontrada"
            )

        db.delete(alerta)
        db.commit()

        return {
            "mensaje": "Alerta eliminada correctamente"
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()