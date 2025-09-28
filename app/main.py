from fastapi import FastAPI
from app.routes import auth

app = FastAPI()

# routers
app.include_router(auth.router)

@app.get('/')
def root():
    return {"status":"OK"}
