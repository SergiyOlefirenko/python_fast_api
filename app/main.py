from typing import List, Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from . import schemas 
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from app.routers import user, post

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "Hellow world!"}
