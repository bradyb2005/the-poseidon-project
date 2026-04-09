from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.restaurant_router import router as restaurant_router
from backend.routes.search_routes import router as search_router
from backend.routes.notifications_router import router as notification_router
from backend.routes.admin_router import router as admin_router   # ADD THIS
from backend.routes.payment_router import router as payment_router
from backend.routes.delivery_router import router as delivery_router
from backend.routes.review_routes import router as review_router
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.items_routes import router as items_routes
from backend.routes.user_routes import router as user_router

app = FastAPI(title="The Poseidon Project")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(restaurant_router)
app.include_router(search_router)
app.include_router(notification_router)
app.include_router(admin_router)   # ADD THIS
app.include_router(payment_router)
app.include_router(delivery_router)
app.include_router(review_router)
app.include_router(items_routes)

@app.get("/")
def root():
    return {"message": "Welcome to The Poseidon Project"}

@app.get("/health")
def health():
    return {"status": "ok"}