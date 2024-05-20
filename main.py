from fastapi import FastAPI
from rotas import router as rotas


# uvicorn main:app --reload
app = FastAPI()

@app.get("/")
def home():
    return "Bem vindo a api do sistema da Barbearia do Pedro!"


app.include_router(rotas)

