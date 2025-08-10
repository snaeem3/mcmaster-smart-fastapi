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
# models.Base.metadata.create_all(bind=engine)
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


# def get_webpage(url):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#         'Accept-Language': 'en-US,en;q=0.5',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Connection': 'keep-alive',
#         'Upgrade-Insecure-Requests': '1',
#     }

#     try:
#         session = requests.Session()
#         response = session.get(
#             url,
#             headers=headers,
#             timeout=10,
#             allow_redirects=True
#         )
#         response.raise_for_status()
#         return response.text
    
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching page: {e}")
#         return None

# @app.post("/search-feedback/")
# def create_feedback(feedback: Feedback):
#     return {"message": f"{feedback.mcmasterID} returned {feedback.mscID} {":)" if feedback.positiveFeedback else ":("}"}
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

@app.post("/items/")
def create_item(name: str, db: Session = Depends(deps.get_db)):
    new_item = models.Item(name=name)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item