from fastapi import APIRouter
from fastapi import Response
from auth import Conect
from auth import TokenAuth
from fastapi import HTTPException, status
from auth.Modulos.Validador import validar_dado as vd

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
    
    dados = dados.get_generico('clientes')
    conteudo = f'"total":{len(dados)}, "records":{dados}'
    return Response(conteudo, 200)


@router.post("/cliente")
async def post_cliente(token, nome:str, email:str="", telefone:str="", data_nascimento:str="", observacao:str=""):
    token_auth = TokenAuth(token)
    if not token_auth.valido:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Invalido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    query = {
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "nascimento": data_nascimento,
        "observacao": observacao,
    }

    validacao = {
        "nome": vd.validar_nome(nome),
        "email": vd.validar_email(email),
        "telefone": vd.validar_numero(telefone),
        "data_nascimento": vd.validar_data_nasc(data_nascimento),
        "observacao": vd.validar_obs(observacao),
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
    
    res = dados.post_generico(tabela='cliente', dados=query)
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
    

@router.patch("/cliente")
async def patch_cliente(token, nome:str="", email:str="", telefone:str="", data_nascimento:str="", observacao:str=""):
    token_auth = TokenAuth(token)
    if not token_auth.valido:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Invalido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    dados = Conect()
    dados.conectar()
    
    res = dados.patch_cliente(dados= {
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "data_nascimento": data_nascimento,
        "observacao": observacao,
    }, id=id)
    if res == 2:
        conteudo = "ERRO QUERY VAZIA"
        status_code = status.HTTP_400_BAD_REQUEST
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
    
