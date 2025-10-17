"""
module: main.py
purpose: contain the main application
"""

from fastapi import FastAPI
from app.routes import auth, users

app = FastAPI()

# routers
app.include_router(auth.router)
app.include_router(users.router)

@app.get('/')
def root():
    return {"status":"OK"}
