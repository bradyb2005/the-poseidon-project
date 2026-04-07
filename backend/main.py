from fastapi import FastAPI
from backend.routes.restaurant_router import router as restaurant_router
from backend.routes.search_routes import router as search_router
from backend.routes.notifications_router import router as notification_router

app = FastAPI(title="The Poseidon Project")

app.include_router(restaurant_router)
app.include_router(search_router)
app.include_router(notification_router)

@app.get("/")
def root():
    return {"message": "Welcome to The Poseidon Project"}

@app.get("/health")
def health():
    return {"status": "ok"}