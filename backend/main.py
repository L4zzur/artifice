from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1 import api_router
from core.config import settings

app = FastAPI(
    title="Artifice Toolkit API",
    description="Many useful tools for many purposes",
    version=settings.version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {
        "message": "Artifice Toolkit API",
        "debug": settings.debug,
        "version": settings.version,
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


@app.get("/health")
@app.head("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.run.host, port=settings.run.port)
