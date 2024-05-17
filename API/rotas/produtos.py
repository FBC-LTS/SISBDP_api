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
        body = df.to_dict('records')
    if code == "004":
        status_code = 204
        body = {"ERRO":msg}
    if code == "000":
        status_code = 500
        body = {"ERRO":f"EXEC - GET PRODUTOS:\nERROR: INESPERADO :(\n000"}
    
    
    return Response(
        content=body, status_code=status_code
    )

