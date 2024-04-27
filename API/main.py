from fastapi import FastAPI

# uvicorn main:app --reload
app = FastAPI()

@app.get("/")
def home():
    return "Bem vindo a api do sistema da Barbearia do Pedro!"

@app.get("/hello-world")
def hello_world():
    return "Hello World!"
