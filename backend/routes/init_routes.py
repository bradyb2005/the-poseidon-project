from backend.routes.user_routes import router as user_router
app.include_router(user_router)
#whats happening here iwth the user_router is that we are simply adding the user-related routes (register, login) to our main FastAPI app. 
