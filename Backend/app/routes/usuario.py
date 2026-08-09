from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
import traceback


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios():
    db: Session = SessionLocal()

    try:
        return db.query(Usuario).all()

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.get("/{idusuario}", response_model=UsuarioResponse)
def obtener_usuario(idusuario: int):
    db: Session = SessionLocal()

    try:
        usuario = db.query(Usuario).filter(
            Usuario.idusuario == idusuario
        ).first()

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        return usuario

    except HTTPException:
        raise

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.post("/", response_model=UsuarioResponse, status_code=201)
def crear_usuario(usuario: UsuarioCreate):
    db: Session = SessionLocal()

    try:
        nuevo_usuario = Usuario(
            nombres=usuario.nombres,
            apellidos=usuario.apellidos,
            correo=usuario.correo,
            contrasenia=usuario.contrasenia,
            telefono=usuario.telefono,
            estadoactual=usuario.estadoactual,
            idrol=usuario.idrol
        )

        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)

        return nuevo_usuario

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.put("/{idusuario}", response_model=UsuarioResponse)
def actualizar_usuario(
    idusuario: int,
    datos: UsuarioCreate
):
    db: Session = SessionLocal()

    try:
        usuario = db.query(Usuario).filter(
            Usuario.idusuario == idusuario
        ).first()

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        usuario.nombres = datos.nombres
        usuario.apellidos = datos.apellidos
        usuario.correo = datos.correo
        usuario.contrasenia = datos.contrasenia
        usuario.telefono = datos.telefono
        usuario.estadoactual = datos.estadoactual
        usuario.idrol = datos.idrol

        db.commit()
        db.refresh(usuario)

        return usuario

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.delete("/{idusuario}")
def eliminar_usuario(idusuario: int):
    db: Session = SessionLocal()

    try:
        usuario = db.query(Usuario).filter(
            Usuario.idusuario == idusuario
        ).first()

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        db.delete(usuario)
        db.commit()

        return {
            "mensaje": "Usuario eliminado correctamente"
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()

@router.get("/{idusuario}/detalle")
def detalle_usuario(idusuario: int):
    db: Session = SessionLocal()

    try:
        usuario = db.query(Usuario).filter(
            Usuario.idusuario == idusuario
        ).first()

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        return {
            "idusuario": usuario.idusuario,
            "nombres": usuario.nombres,
            "apellidos": usuario.apellidos,
            "correo": usuario.correo,
            "estadoactual": usuario.estadoactual,
            "rol": usuario.rol,
            "especialidades": usuario.especialidades,
            "expedientes": usuario.expedientes
        }

    except HTTPException:
        raise

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()