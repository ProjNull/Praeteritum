from sqlalchemy import Column, Integer, ForeignKey, String

from .. import Base

class Votes(Base):
    __tablename__ = "votes"
    vote_id = Column(Integer, primary_key=True, autoincrement= "auto", nullable=False)
    user_id = Column(String, nullable=False)
    retro_id = Column(Integer, ForeignKey("retros.retro_id"), nullable=False)
    note_id = Column(Integer, ForeignKey("notes.note_id"), nullable=False)

    def __init__(self, user_id, retro_id, note_id):
        self.user_id = user_id
        self.retro_id = retro_id
        self.note_id = note_id