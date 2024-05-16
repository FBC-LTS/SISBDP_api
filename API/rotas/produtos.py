from fastapi import APIRouter
from fastapi import Response
from auth import Conect
import json

router = APIRouter()



@router.get("/produtos.json")
async def get_produtos():
    dados = Conect()
    dados.conectar()
    val, produtos = dados.get_produtos()
    #conectar bd puxar produtos e serviços
    if val:
        res = produtos.to_dict('records')

    else:
        return Response(
            "ERRO AO PEGAR DADOS", status_code=204
        )

    return Response(
        f'"total_itens": {len(res)},"Produtos": {res}'
    )
        

