from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class user(Base):
    __tablename__ = "userModel"

    uID = Column(Integer, nullable=False, unique=True, primary_key=True)