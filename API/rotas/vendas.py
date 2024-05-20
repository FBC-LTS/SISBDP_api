import json
from urllib.parse import unquote
from fastapi import APIRouter
from fastapi import Response
from auth import Conect
from auth import TokenAuth
from fastapi import HTTPException, status
from auth.Modulos.Validador import validar_dado as vd

router = APIRouter()


@router.get("/vendas.json")
async def get_vendas(token):
    token_auth = TokenAuth(token)
    if not token_auth.valido:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Invalido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    dados = Conect()
    dados.conectar()
    
    dados = dados.get_vendas()
    conteudo = f'"total":{len(dados)}, "records":{dados}'
    return Response(conteudo, 200)


@router.get("/venda.json")
async def get_venda(token, id:int):
    token_auth = TokenAuth(token)
    if not token_auth.valido:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Invalido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    dados = Conect()
    dados.conectar()
    if id < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID Invalido",
        )
    
    dados, val = dados.get_vendas(id)
    if not val:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="SEM ESTOQUE",
        )
    conteudo = f'"total":{len(dados)}, "records":{dados}'
    return Response(conteudo, 200)


@router.post("/venda")
async def post_venda(token, id_cliente:int, id_vendedor:int, carrinho:str, desconto_venda:float=0):
    """
    carrinho = {
        "produtos": [
            {"id":int,"quantidade": int},
            ...
            ]
        "servicos": [ 
            {"id":int,"quantidade": int},
            ...
            ]
        }
    """
    token_auth = TokenAuth(token)
    if not token_auth.valido:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Invalido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not vd.esta_entre(desconto_venda, 0, 1):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Desconto invalido"
        )
    carrinho_decod = unquote(carrinho)

    if carrinho_decod.startswith("'") and carrinho_decod.endswith("'"):
        carrinho_decod = carrinho_decod[1:-1]
    
    if not vd.validar_carrinho(carrinho_decod):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="JSON carrinho invalido"
        )

    query = {
        'id_cliente': id_cliente,
        'id_vendedor': id_vendedor,
        'carrinho': json.loads(carrinho_decod),
        'desconto_venda': desconto_venda
    }

    dados = Conect()
    dados.conectar()
    res = dados.post_venda(query)
    if res:
        conteudo = "SUCCESS"
        status_code = 200
    else:
        conteudo = "ERRO INESPERADO"
        status_code = 500

    return Response(
        content=conteudo,
        status_code=status_code
    )
    

