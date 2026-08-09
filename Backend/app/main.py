from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.routes.rol import router as rol_router
from app.routes.usuario import router as usuario_router
from app.routes.especialidad import router as especialidad_router
from app.routes.cliente import router as cliente_router
from app.routes.expediente import router as expediente_router
from app.routes.documento import router as documento_router
from app.routes.actuacion import router as actuacion_router
from app.routes.audiencia import router as audiencia_router
from app.routes.alerta import router as alerta_router
from app.routes.usuario_especialidad import router as usuario_especialidad_router
from app.routes.expediente_usuario import router as expediente_usuario_router
from app.routes.login import router as login_router


app = FastAPI(
    title="Sistema Jurídico",
    description="API para la gestión del bufete jurídico",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rol_router)
app.include_router(usuario_router)
app.include_router(especialidad_router)
app.include_router(cliente_router)
app.include_router(expediente_router)
app.include_router(documento_router)
app.include_router(actuacion_router)
app.include_router(audiencia_router)
app.include_router(alerta_router)
app.include_router(usuario_especialidad_router)
app.include_router(expediente_usuario_router)
app.include_router(login_router)

@app.on_event("startup")
def conectar_bd():
    try:
        with engine.connect() as connection:
            print("✅ Conexión exitosa con PostgreSQL")
    except Exception as e:
        print("❌ Error al conectar con PostgreSQL:")
        print(e)

@app.get("/")
def inicio():
    return {
        "mensaje": "Petro"
    }