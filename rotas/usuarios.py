from fastapi import APIRouter
from fastapi import Response
from auth import Conect
import os
import dotenv

router = APIRouter()
dotenv.load_dotenv(dotenv.find_dotenv())
APP_KEY = os.getenv("app_key")

@router.post("/usuario")
async def post_usuario(nome:str, email:str, telefone:str, senha:str, app_key:str):
    if app_key != APP_KEY:
        return Response("NÃO AUTORIZADO", 401)
    dados = Conect()
    dados.conectar()
    validade = dados.post_usuario(nome=str(nome), email=str(email), telefone=str(telefone), senha=str(senha))
    conteudo = f'"email":{validade[0]},"telefone":{validade[1]},"senha":{validade[2]},"registro":{validade[3]}'
    if validade[-1]:
        status_code = 200
    else: 
        status_code = 400
    return Response(
        content=conteudo,
        status_code=status_code
    )
