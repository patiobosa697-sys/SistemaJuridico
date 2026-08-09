from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.rol import Rol
from app.schemas.rol import RolCreate, RolResponse
import traceback


router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)


@router.get("/", response_model=list[RolResponse])
def listar_roles():
    db: Session = SessionLocal()

    try:
        return db.query(Rol).all()

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.get("/{idrol}", response_model=RolResponse)
def obtener_rol(idrol: int):
    db: Session = SessionLocal()

    try:
        rol = db.query(Rol).filter(Rol.idrol == idrol).first()

        if not rol:
            raise HTTPException(
                status_code=404,
                detail="Rol no encontrado"
            )

        return rol

    except HTTPException:
        raise

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.post("/", response_model=RolResponse, status_code=201)
def crear_rol(rol: RolCreate):
    db: Session = SessionLocal()

    try:
        nuevo_rol = Rol(
            nombrerol=rol.nombrerol
        )

        db.add(nuevo_rol)
        db.commit()
        db.refresh(nuevo_rol)

        return nuevo_rol

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.put("/{idrol}", response_model=RolResponse)
def actualizar_rol(idrol: int, datos: RolCreate):
    db: Session = SessionLocal()

    try:
        rol = db.query(Rol).filter(Rol.idrol == idrol).first()

        if not rol:
            raise HTTPException(
                status_code=404,
                detail="Rol no encontrado"
            )

        rol.nombrerol = datos.nombrerol

        db.commit()
        db.refresh(rol)

        return rol

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.delete("/{idrol}")
def eliminar_rol(idrol: int):
    db: Session = SessionLocal()

    try:
        rol = db.query(Rol).filter(Rol.idrol == idrol).first()

        if not rol:
            raise HTTPException(
                status_code=404,
                detail="Rol no encontrado"
            )

        db.delete(rol)
        db.commit()

        return {
            "mensaje": "Rol eliminado correctamente"
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()