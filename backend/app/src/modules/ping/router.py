from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

router = APIRouter()

@router.get("/")
def ping():
    return JSONResponse(
        content={"status": "Server is online"},
        status_code=200
    )