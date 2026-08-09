from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.expediente import Expediente
from app.schemas.expediente import ExpedienteCreate, ExpedienteResponse
import traceback
from app.models.cliente import Cliente
from fastapi import APIRouter, HTTPException, Query


router = APIRouter(
    prefix="/expedientes",
    tags=["Expedientes"]
)


@router.get("/", response_model=list[ExpedienteResponse])
def listar_expedientes():
    db: Session = SessionLocal()

    try:
        return db.query(Expediente).all()

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()

@router.get("/buscar")
def buscar_expedientes(
    radicado: str | None = Query(
        None,
        description="Número de radicado judicial del expediente. Ejemplo: 2026-000000"
    ),
    documento: str | None = Query(
        None,
        description="Número de documento de identidad del cliente. Ejemplo: 1234567890"
    ),
    nombre: str | None = Query(
        None,
        description="Nombre o apellido del cliente.Algún Nombre o Apellido"
    ),
    codigo: str | None = Query(
        None,
        description="Código interno del expediente. Ejemplo: EXP-001"
    )
):
    db: Session = SessionLocal()

    try:
        consulta = db.query(Expediente).join(
            Expediente.cliente
        )

        if radicado:
            consulta = consulta.filter(
                Expediente.numeroradicado.ilike(f"%{radicado}%")
            )

        if documento:
            consulta = consulta.filter(
                Cliente.numdocumento.ilike(f"%{documento}%")
            )

        if nombre:
            consulta = consulta.filter(
                (Cliente.nombres.ilike(f"%{nombre}%")) |
                (Cliente.apellidos.ilike(f"%{nombre}%"))
            )

        if codigo:
            consulta = consulta.filter(
                Expediente.codigointerno.ilike(f"%{codigo}%")
            )

        return consulta.all()

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.get("/{idexpediente}", response_model=ExpedienteResponse)
def obtener_expediente(idexpediente: int):
    db: Session = SessionLocal()

    try:
        expediente = db.query(Expediente).filter(
            Expediente.idexpediente == idexpediente
        ).first()

        if not expediente:
            raise HTTPException(
                status_code=404,
                detail="Expediente no encontrado"
            )

        return expediente

    except HTTPException:
        raise

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.post("/", response_model=ExpedienteResponse, status_code=201)
def crear_expediente(datos: ExpedienteCreate):
    db: Session = SessionLocal()

    try:
        nuevo_expediente = Expediente(
            codigointerno=datos.codigointerno,
            numeroradicado=datos.numeroradicado,
            asunto=datos.asunto,
            descripcion=datos.descripcion,
            estado=datos.estado,
            fechaapertura=datos.fechaapertura,
            fechacierre=datos.fechacierre,
            idcliente=datos.idcliente,
            idespecialidad=datos.idespecialidad
        )

        db.add(nuevo_expediente)
        db.commit()
        db.refresh(nuevo_expediente)

        return nuevo_expediente

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.put("/{idexpediente}", response_model=ExpedienteResponse)
def actualizar_expediente(
    idexpediente: int,
    datos: ExpedienteCreate
):
    db: Session = SessionLocal()

    try:
        expediente = db.query(Expediente).filter(
            Expediente.idexpediente == idexpediente
        ).first()

        if not expediente:
            raise HTTPException(
                status_code=404,
                detail="Expediente no encontrado"
            )

        expediente.codigointerno = datos.codigointerno
        expediente.numeroradicado = datos.numeroradicado
        expediente.asunto = datos.asunto
        expediente.descripcion = datos.descripcion
        expediente.estado = datos.estado
        expediente.fechaapertura = datos.fechaapertura
        expediente.fechacierre = datos.fechacierre
        expediente.idcliente = datos.idcliente
        expediente.idespecialidad = datos.idespecialidad

        db.commit()
        db.refresh(expediente)

        return expediente

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.delete("/{idexpediente}")
def eliminar_expediente(idexpediente: int):
    db: Session = SessionLocal()

    try:
        expediente = db.query(Expediente).filter(
            Expediente.idexpediente == idexpediente
        ).first()

        if not expediente:
            raise HTTPException(
                status_code=404,
                detail="Expediente no encontrado"
            )

        db.delete(expediente)
        db.commit()

        return {
            "mensaje": "Expediente eliminado correctamente"
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()

@router.get("/{idexpediente}/detalle")
def detalle_expediente(idexpediente: int):
    db: Session = SessionLocal()

    try:
        expediente = db.query(Expediente).filter(
            Expediente.idexpediente == idexpediente
        ).first()

        if not expediente:
            raise HTTPException(
                status_code=404,
                detail="Expediente no encontrado"
            )

        return {
            "idexpediente": expediente.idexpediente,
            "codigointerno": expediente.codigointerno,
            "numeroradicado": expediente.numeroradicado,
            "asunto": expediente.asunto,
            "estado": expediente.estado,
            "cliente": expediente.cliente,
            "especialidad": expediente.especialidad,
            "documentos": expediente.documentos,
            "actuaciones": expediente.actuaciones,
            "audiencias": expediente.audiencias,
            "alertas": expediente.alertas,
            "usuarios_asignados": expediente.usuarios_asignados
        }

    except HTTPException:
        raise

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()

