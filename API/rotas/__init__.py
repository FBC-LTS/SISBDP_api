from fastapi import APIRouter

from .helloWorld import router as hello_world
from .produtos import router as produtos

router = APIRouter()

router.include_router(hello_world)
router.include_router(produtos)
