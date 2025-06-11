from fastapi import FastAPI
from app.routers import search

app = FastAPI(
    title="API de Búsqueda de Jurisprudencia",
    description="Consulta semántica sobre jurisprudencia peruana.",
    version="1.0.0"
)

app.include_router(search.router)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de jurisprudencia."}
