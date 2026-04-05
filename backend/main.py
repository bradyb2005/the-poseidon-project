from fastapi import FastAPI
from backend.routes import restaurant_router, search_routes, payment_router, delivery_router

app = FastAPI(title="The Poseidon Project")

app.include_router(restaurant_router.router)
app.include_router(search_routes.router)
app.include_router(payment_router.router)
app.include_router(delivery_router.router)

@app.get("/")
def root():
    return {"message": "Welcome to The Poseidon Project"}

@app.get("/health")
def health():
    return {"status": "ok"}
