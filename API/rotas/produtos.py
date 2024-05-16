from fastapi import APIRouter

router = APIRouter()

@router.get("/produtos.json")
async def get_produtos():
    #conectar bd puxar produtos e serviços
    return {
        "total_itens": 0,
        "Produtos": {}
        }

