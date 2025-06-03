from sqlalchemy import Column, Integer, String, Text
from database import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    CName = Column(String, nullable=True)
    email = Column(String, nullable=False)
    service = Column(String, nullable=False)
    satisfaction = Column(Integer, nullable=False)
    onTime = Column(String, nullable=False)
    communication = Column(Integer, nullable=False)
    recommend = Column(String, nullable=False)
    liked = Column(Text, nullable=True)
    improve = Column(Text, nullable=True)
    comments = Column(Text, nullable=True)
