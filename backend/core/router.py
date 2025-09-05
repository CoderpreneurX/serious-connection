from fastapi import APIRouter

from .exceptions import JSONException

# Import module routers here
# from modules.auth.routes import router as auth_router
# from modules.groups.routes import router as groups_router
# from modules.messages.routes import router as messages_router

api_router = APIRouter()


# Health check route
@api_router.get("/ping", tags=["health"])
async def ping():
    raise JSONException(message={"title": "Hello", "description": "Sorry bruh, I can't!"}, status_code=400)


# Include module routers (uncomment when ready)
# api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
# api_router.include_router(groups_router, prefix="/groups", tags=["groups"])
# api_router.include_router(messages_router, prefix="/messages", tags=["messages"])
