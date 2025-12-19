from fastapi import APIRouter
from .modules.ping.router import router as ping_router
from .modules.auth.router import router as auth_router

router = APIRouter()

router.include_router(ping_router)
router.include_router(auth_router)