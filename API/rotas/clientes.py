from fastapi import APIRouter
from fastapi import Response
from auth import Conect
from auth import TokenAuth
from fastapi import HTTPException, status

router = APIRouter()

@router.get("/clientes.json")
async def get_clientes(token):
    token_auth = TokenAuth(token)
    if not token_auth.valido:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Invalido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    dados = Conect()
    dados.conectar()
    
    dados = dados.get_clientes()
    conteudo = f'"total":{len(dados)}, "records":{dados}'
    return Response(conteudo, 200)


@router.post("/cliente")
async def post_cliente(token):
    pass