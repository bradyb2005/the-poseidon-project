from fastapi import FastAPI
from backend.routes.restaurant_router import router as restaurant_router
from backend.routes.search_routes import router as search_router
from backend.routes.notifications_router import router as notification_router
from backend.routes.payment_router import router as payment_router
from backend.routes.delivery_router import router as delivery_router
from backend.routes.items_routes import router as items_routes

app = FastAPI(title="The Poseidon Project")

app.include_router(restaurant_router)
app.include_router(search_router)
app.include_router(notification_router)
app.include_router(payment_router)
app.include_router(delivery_router)
app.include_router(items_routes)

@app.get("/")
def root():
    return {"message": "Welcome to The Poseidon Project"}

@app.get("/health")
def health():
    return {"status": "ok"}