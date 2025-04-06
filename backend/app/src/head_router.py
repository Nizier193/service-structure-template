from fastapi import APIRouter
from .modules.ping.router import router as ping_router

router = APIRouter()

router.include_router(ping_router)