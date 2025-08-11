from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.lifespan import lifespan
from app.api.v1 import (
    users,
    auth
)

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Health check endpoint
@app.get("/")
async def health_check():
    return {"message": "Welcome to the E-commerce API!"}
