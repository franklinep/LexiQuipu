from fastapi import FastAPI
from app.routers import search
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API de Búsqueda de Jurisprudencia",
    description="Consulta semántica sobre jurisprudencia peruana.",
    version="1.0.0"
)

app.include_router(search.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # asegurate que el front corra en port:3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de jurisprudencia."}
