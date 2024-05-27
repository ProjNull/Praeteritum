from ..database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean

class SusModel(Base):
    __tablename__ = 'sus'
    ...