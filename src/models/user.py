from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.config.db import Base 

class User(Base):
    __tablename__ = "users"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username= Column(String)
    profile_pic= Column(String, nullable=True)
    about= Column(String, nullable=True)
    hashed_password = Column(String)


