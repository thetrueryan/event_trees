from fastapi import FastAPI
import uvicorn

from src.api.v1.auth_routers import router as auth_router
from src.api.v1.user_routers import router as user_router
from src.api.v1.events_routers import router as event_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(event_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
