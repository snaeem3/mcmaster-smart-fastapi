from sqlalchemy import Boolean, Column, Integer, String
from database import Base

# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True, index=True) # index improves the performance of My SQL
#     username = Column(String(50), unique=True)

# class Post(Base):
#     __tablename__ = 'posts'

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(50))
#     content = Column(String(100))
#     user_id = Column(Integer)

class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True, index=True)
    mcmasterId = Column(String(50))
    mscId = Column(String(50))
    positiveFeedback = Column(Boolean)

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
