from fastapi import APIRouter
from fastapi import Response

router = APIRouter()

@router.get("/hello-world")
async def hello_world():
    return Response(f'Hello World!', 418)
    

@router.post("/hello-world")
async def hello_world_json(name):
    msg = "Hello World!"
    if name:
        msg += f' Wellcome {str(name).replace('"', '')}!'
    return Response(f'"message": {msg}', 418)