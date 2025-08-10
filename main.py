from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import BaseModel
from typing import Annotated
import models, database, deps
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import requests

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Feedback(BaseModel):
    mcmasterId: str
    mscId: str | None
    positiveFeedback: bool

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/search-feedback/", status_code=status.HTTP_201_CREATED)
async def create_feedback(feedback: Feedback, db: Session = Depends(deps.get_db)):
    db_feedback = models.Feedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@app.get("/search-feedback/")
def get_feedback(db: Session = Depends(deps.get_db)):
    return db.query(models.Feedback).all()
