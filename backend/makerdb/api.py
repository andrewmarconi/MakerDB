from fastapi import FastAPI
from parts.router import router as parts_router
from inventory.router import router as inventory_router
from projects.router import router as projects_router
from procurement.router import router as procurement_router
from core.router import router as core_router

app = FastAPI(title="MakerDB API", version="0.1.0")

app.include_router(parts_router)
app.include_router(inventory_router)
app.include_router(projects_router)
app.include_router(procurement_router)
app.include_router(core_router, prefix="/companies", tags=["Companies"])


@app.get("/health")
async def health():
    return {"status": "ok"}
