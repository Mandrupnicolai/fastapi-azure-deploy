from fastapi import FastAPI
from app.routers import health

app = FastAPI(
    title="fastapi-azure-deploy",
    description="A production-ready FastAPI service deployed on Azure Container Apps.",
    version="1.0.0",
)

app.include_router(health.router)


@app.get("/")
def root():
    return {"message": "FastAPI is running on Azure Container Apps 🚀"}
