
from fastapi import FastAPI
from .routers import router

app = FastAPI()

app.include_router(router)

# Optionally add a health check
@app.get("/health")
def health():
    return {"status": "ok"}

