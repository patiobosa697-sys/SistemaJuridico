from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.documento import Documento
from app.schemas.documento import DocumentoCreate, DocumentoResponse
import traceback


router = APIRouter(
    prefix="/documentos",
    tags=["Documentos"]
)


@router.get("/", response_model=list[DocumentoResponse])
def listar_documentos():
    db: Session = SessionLocal()

    try:
        return db.query(Documento).all()

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.get("/{iddocumento}", response_model=DocumentoResponse)
def obtener_documento(iddocumento: int):
    db: Session = SessionLocal()

    try:
        documento = db.query(Documento).filter(
            Documento.iddocumento == iddocumento
        ).first()

        if not documento:
            raise HTTPException(
                status_code=404,
                detail="Documento no encontrado"
            )

        return documento

    except HTTPException:
        raise

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.post("/", response_model=DocumentoResponse, status_code=201)
def crear_documento(datos: DocumentoCreate):
    db: Session = SessionLocal()

    try:
        nuevo_documento = Documento(
            nombre=datos.nombre,
            tipodocumento=datos.tipodocumento,
            rutaarchivo=datos.rutaarchivo,
            fechasubida=datos.fechasubida,
            descripcion=datos.descripcion,
            idexpediente=datos.idexpediente
        )

        db.add(nuevo_documento)
        db.commit()
        db.refresh(nuevo_documento)

        return nuevo_documento

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.put("/{iddocumento}", response_model=DocumentoResponse)
def actualizar_documento(
    iddocumento: int,
    datos: DocumentoCreate
):
    db: Session = SessionLocal()

    try:
        documento = db.query(Documento).filter(
            Documento.iddocumento == iddocumento
        ).first()

        if not documento:
            raise HTTPException(
                status_code=404,
                detail="Documento no encontrado"
            )

        documento.nombre = datos.nombre
        documento.tipodocumento = datos.tipodocumento
        documento.rutaarchivo = datos.rutaarchivo
        documento.fechasubida = datos.fechasubida
        documento.descripcion = datos.descripcion
        documento.idexpediente = datos.idexpediente

        db.commit()
        db.refresh(documento)

        return documento

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.delete("/{iddocumento}")
def eliminar_documento(iddocumento: int):
    db: Session = SessionLocal()

    try:
        documento = db.query(Documento).filter(
            Documento.iddocumento == iddocumento
        ).first()

        if not documento:
            raise HTTPException(
                status_code=404,
                detail="Documento no encontrado"
            )

        db.delete(documento)
        db.commit()

        return {
            "mensaje": "Documento eliminado correctamente"
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()