from fastapi import FastAPI

app = FastAPI(title="The Poseidon Project")

@app.get("/")
def root():
    return {"message": "Welcome to The Poseidon Project"}