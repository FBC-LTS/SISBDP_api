from fastapi import APIRouter

router = APIRouter()

@router.get("/hello-world")
async def hello_world():
    return "Hello World!"

@router.get("/hello-world.json")
async def hello_world_json(name):
    msg = "Hello World!"
    if name:
        msg += f' Wellcome {str(name).replace('"', '')}!'
    return {"message": msg}