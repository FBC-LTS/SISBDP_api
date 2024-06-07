from fastapi import APIRouter
from fastapi import Response
from auth import Conect
from auth import TokenAuth
from auth.Modulos.Validador.validar_dado import validar_produtos, gestor_codigos
from fastapi import HTTPException, status
import pandas as pd

router = APIRouter()

TIPOS = ["servico", "produto"]

@router.get("/produtos.json")
async def get_produtos(token):
    token_auth = TokenAuth(token)
    if not token_auth.valido:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Invalido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    dados = Conect()
    dados.conectar()
    produtos, msg = dados.get_produtos()
    return analizador(produtos, msg)

@router.get("/produto.json")
async def get_produto(token, tipo, id):
    token_auth = TokenAuth(token)
    if not token_auth.valido:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Invalido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if tipo not in TIPOS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo invalido",
        )
    dados = Conect()
    dados.conectar()
    produto, msg = dados.get_produto(tipo, id)
    return analizador(produto, msg) 
        

def analizador(df:pd.DataFrame, msg:str):
    code = msg[-3:]
    if code == "100":
        status_code = 200
        content = df.to_dict("records")
        body = f'"total_itens":{len(content)},"records":{content}'
    if code == "004":
        status_code = 503
        body = f'"ERRO":{msg}'
    if code == "000":
        status_code = 500
        msg = f"EXEC - GET PRODUTOS:\nERROR: INESPERADO :(\n000"
        body = f'"ERRO":{msg}'
    
    
    return Response(
        content=body, status_code=status_code
    )


@router.post("/produtos")
async def post_produtos(token, tipo:str, nome:str, preco:float, categoria:str="", quantidade:int=-1, obs:str=""):
    token_auth = TokenAuth(token)
    if not token_auth.valido:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Invalido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    dados = Conect()
    dados.conectar()
    codigo = validar_produtos(tipo, nome, preco, categoria, quantidade, obs)
    if codigo == "100":
        dados.post_produtos(
            tipo=tipo,
            dados={
                "nome":nome,
                "preco":preco,
                "categoria":categoria,
                "quantidade":quantidade,
                "observacao":obs
            }
        )
        return Response(content="PRODUTO REGISTRADO", status_code=200)
    
    return Response(
        content=f'{gestor_codigos(codigo)}', status_code=status.HTTP_400_BAD_REQUEST
    )


@router.delete("/produtos")
async def delete_produtos(token, tipo:str, id:int):
    token_auth = TokenAuth(token)
    if not token_auth.valido:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Invalido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if tipo not in TIPOS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo invalido",
        )
    dados = Conect()
    dados.conectar()
    dados.delete_generico(tipo, id)

    return Response(
        content="PRODUTO DELETADO", status_code=200)


@router.patch("/produtos")
async def path_produtos(token, tipo:str, id:int, nome:str="", preco:float=-1, categoria:str="", quantidade:int=-1, obs:str=""):
    token_auth = TokenAuth(token)
    if not token_auth.valido:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Invalido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if tipo not in TIPOS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo invalido",
        )
    

    dados = Conect() 
    dados.conectar()
    dados.patch_produtos(tipo, id=id, dados={
        "nome":nome,
        "preco":preco,
        "categoria":categoria,
        "quantidade":quantidade,
        "observacao":obs
    })
    
    return Response(content="PRODUTO ATUALIZADO", status_code=200)