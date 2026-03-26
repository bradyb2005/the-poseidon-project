from fastapi import FastAPI
from backend.routes import restaurant_router

app = FastAPI(title="The Poseidon Project")

app.include_router(restaurant_router.router)

@app.get("/")
def root():
    return {"message": "Welcome to The Poseidon Project"}

@app.get("/health")
def health():
    return {"status": "ok"}
