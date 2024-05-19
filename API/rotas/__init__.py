from fastapi import APIRouter

from .helloWorld import router as hello_world
from .produtos import router as produtos
from .usuarios import router as usuarios
from .token import router as token
from .clientes import router as clientes


router = APIRouter()

router.include_router(hello_world)
router.include_router(produtos)
router.include_router(usuarios)
router.include_router(token)
router.include_router(clientes)
