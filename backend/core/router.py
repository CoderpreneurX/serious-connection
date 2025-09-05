from fastapi import APIRouter
from fastapi.responses import JSONResponse

from .email import test_send_email

# Import module routers here
# from modules.auth.routes import router as auth_router
# from modules.groups.routes import router as groups_router
# from modules.messages.routes import router as messages_router

api_router = APIRouter()


# Health check route
@api_router.get("/ping", tags=["health"])
async def ping():
    await test_send_email()
    return JSONResponse(content={"success": True, "message": "Pong!"})


# Include module routers (uncomment when ready)
# api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
# api_router.include_router(groups_router, prefix="/groups", tags=["groups"])
# api_router.include_router(messages_router, prefix="/messages", tags=["messages"])
