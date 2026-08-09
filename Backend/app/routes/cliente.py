from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteResponse
import traceback


router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)


@router.get("/", response_model=list[ClienteResponse])
def listar_clientes():
    db: Session = SessionLocal()

    try:
        return db.query(Cliente).all()

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.get("/{idcliente}", response_model=ClienteResponse)
def obtener_cliente(idcliente: int):
    db: Session = SessionLocal()

    try:
        cliente = db.query(Cliente).filter(
            Cliente.idcliente == idcliente
        ).first()

        if not cliente:
            raise HTTPException(
                status_code=404,
                detail="Cliente no encontrado"
            )

        return cliente

    except HTTPException:
        raise

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.post("/", response_model=ClienteResponse, status_code=201)
def crear_cliente(cliente: ClienteCreate):
    db: Session = SessionLocal()

    try:
        nuevo_cliente = Cliente(
            tipodocumento=cliente.tipodocumento,
            numdocumento=cliente.numdocumento,
            nombres=cliente.nombres,
            apellidos=cliente.apellidos,
            telefono=cliente.telefono,
            correo=cliente.correo,
            direccion=cliente.direccion
        )

        db.add(nuevo_cliente)
        db.commit()
        db.refresh(nuevo_cliente)

        return nuevo_cliente

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.put("/{idcliente}", response_model=ClienteResponse)
def actualizar_cliente(
    idcliente: int,
    datos: ClienteCreate
):
    db: Session = SessionLocal()

    try:
        cliente = db.query(Cliente).filter(
            Cliente.idcliente == idcliente
        ).first()

        if not cliente:
            raise HTTPException(
                status_code=404,
                detail="Cliente no encontrado"
            )

        cliente.tipodocumento = datos.tipodocumento
        cliente.numdocumento = datos.numdocumento
        cliente.nombres = datos.nombres
        cliente.apellidos = datos.apellidos
        cliente.telefono = datos.telefono
        cliente.correo = datos.correo
        cliente.direccion = datos.direccion

        db.commit()
        db.refresh(cliente)

        return cliente

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.delete("/{idcliente}")
def eliminar_cliente(idcliente: int):
    db: Session = SessionLocal()

    try:
        cliente = db.query(Cliente).filter(
            Cliente.idcliente == idcliente
        ).first()

        if not cliente:
            raise HTTPException(
                status_code=404,
                detail="Cliente no encontrado"
            )

        db.delete(cliente)
        db.commit()

        return {
            "mensaje": "Cliente eliminado correctamente"
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()