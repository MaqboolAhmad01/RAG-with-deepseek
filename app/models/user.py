from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config.db import Base 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username: Column(String)
    profile_pic: Column(String, nullable=True)
    about: Column(String, nullable=True)
    hashed_password = Column(String)


