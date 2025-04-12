from sqlalchemy import Column, Integer, String, ForeignKey

from .. import Base

class Notes(Base):
    __tablename__ = "notes"
    note_id = Column(Integer, primary_key=True, autoincrement= "auto", nullable=False)
    user_id = Column(String, nullable=False)
    retro_id = Column(Integer, ForeignKey("retros.retro_id"), nullable=False)
    content = Column(String(250), nullable=False)
    column = Column(Integer, nullable=False)
    
    def __init__(self, user_id, retro_id, content, column):
        self.user_id = user_id
        self.retro_id = retro_id
        self.content = content
        self.column = column