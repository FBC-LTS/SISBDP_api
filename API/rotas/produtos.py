from fastapi import APIRouter
from fastapi import Response
from auth import Conect
import json
import pandas as pd

router = APIRouter()



@router.get("/produtos.json")
async def get_produtos():
    dados = Conect()
    dados.conectar()
    produtos, msg = dados.get_produtos()
    return analizador(produtos, msg)
        

def analizador(df:pd.DataFrame, msg:str):
    code = msg[-3:]
    if code == "100":
        status_code = 200
        content = df.to_dict("records")
        body = f'"total_itens":{len(content)},"records":{content}'
    if code == "004":
        status_code = 204
        body = f'"ERRO":{msg}'
    if code == "000":
        status_code = 500
        msg = f"EXEC - GET PRODUTOS:\nERROR: INESPERADO :(\n000"
        body = f'"ERRO":{msg}'
    
    
    return Response(
        content=body, status_code=status_code
    )

@router.post("/produtos")
async def post_produtos():
    dados = Conect()
    dados.conectar()
    return Response(
        content="EM PRODUÇÃO", status_code=204
    )

@router.patch("/produtos")
async def path_produtos():
    dados = Conect()
    dados.conectar()
    return Response(
        content="EM PRODUÇÃO", status_code=204
    )