from fastapi import FastAPI
from db.database import Base, engine
from db.seed import seed_data
from routes import auth

app = FastAPI(title="Sistema de Agendamento Escolar")

Base.metadata.create_all(bind=engine)
seed_data()

app.include_router(auth.router)

@app.get("/")
def root():
    return {"msg": "API funcionando ✅"}
