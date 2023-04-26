from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Question(Base):
    __tablename__ = "question"

    id:int = Column(Integer, primary_key=True)
    subject:str = Column(String, nullable=False)
    content:str = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)

class Answer(Base):
    __tablename__ = "answer"

    id:int = Column(Integer, primary_key=True)
    content:str = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"))
    question = relationship("Question", backref="answers")

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique= True, nullable=False)

    