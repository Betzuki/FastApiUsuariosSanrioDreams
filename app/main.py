from fastapi import FastAPI
from app.routers import usuarios

app = FastAPI(
    title="API para gestión de usuarios",
    version="1.0.0",
    description="API para gestionar usuarios usando FastAPI y Oracle"
)


app.include_router(usuarios.router)