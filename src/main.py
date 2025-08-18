from fastapi import FastAPI
import uvicorn

from api.v1.auth_routers import router as auth_router

app = FastAPI()

app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)