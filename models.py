from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True, index=True)
    mcmasterId = Column(String(50))
    mscId = Column(String(50))
    positiveFeedback = Column(Boolean)
