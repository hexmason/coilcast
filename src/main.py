import uvicorn
from fastapi import FastAPI

from application.config.settings import Settings
from presentation.api.subsonic.routers import subsonic_router

settings = Settings()
app = FastAPI()
app.include_router(subsonic_router, prefix="/rest", tags=["rest"])

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=settings.HTTP_PORT)
