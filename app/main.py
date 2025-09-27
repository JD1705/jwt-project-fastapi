from fastapi import FastAPI
from routes import auth

app = FastAPI()

# routers
app.include_router(auth.router)

@app.get('/')
def root():
    return {"status":"OK"}
