from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    slug = Column(String, unique=True, index=True)
    tasks = relationship("Task", back_populates="user")  # Связь с таблицей Task

