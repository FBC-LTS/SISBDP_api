from fastapi import APIRouter
from fastapi import Response
from auth.Auth import Auth
from fastapi import HTTPException, status


router = APIRouter()

@router.get("/token")
async def get_token(email, senha):
    auth = Auth(email, senha)
    if not auth.autenticado:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha errados",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = auth.token()
    conteudo = f'"token": {token}, "token_type": "bearer"'

    return Response(conteudo, headers={"WWW-Authenticate": "Bearer"})

