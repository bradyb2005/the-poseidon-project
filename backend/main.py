from fastapi import FastAPI
from backend.routes import items_routes, restaurant_router, search_routes

app = FastAPI(title="The Poseidon Project")

app.include_router(restaurant_router.router)
app.include_router(search_routes.router)
app.include_router(items_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to The Poseidon Project"}

@app.get("/health")
def health():
    return {"status": "ok"}
