from fastapi import APIRouter
from fastapi import Response
from auth import Conect
from auth import TokenAuth
from fastapi import HTTPException, status
from auth.Modulos.Validador import validar_dado as vd

router = APIRouter()


@router.get("/gastos.json")
async def get_gastos(token):
    token_auth = TokenAuth(token)
    if not token_auth.valido:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Invalido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    dados = Conect()
    dados.conectar()
    
    dados = dados.get_generico('gastos')
    conteudo = f'"total":{len(dados)}, "records":{dados}'
    return Response(conteudo, 200)

@router.post("/gasto")
async def post_gasto(token, nome:str, preco:float, data:str="", descricao:str=""):
    token_auth = TokenAuth(token)
    if not token_auth.valido:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Invalido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # nome_gasto, preco_gasto, descricao_gasto, data_gasto
    query = {
        "nome": nome,
        "preco": preco,
        "descricao": descricao,
        "data": data,
    }

    validacao = {
        "nome": vd.validar_nome(nome),
        "preco": vd.validar_preco(preco),
        "descricao": vd.validar_obs(descricao),
        "data": vd.validar_data_nasc(data),
    }

    keys, valido, query = vd.validar_query_cliente(validacao, query)
    if not valido:
        conteudo = "DADOS INVALIDOS:"
        for key in keys:
            conteudo += f' {key}'
        conteudo += "."
        return Response(
            content=conteudo,
            status_code=status.HTTP_406_NOT_ACCEPTABLE
        )
    
    dados = Conect()
    dados.conectar()
    
    res = dados.post_generico(tabela='gasto', dados=query)
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
    