from sqlalchemy import Column, Integer, ForeignKey

from .. import Base

class Votes(Base):
    __tablename__ = "votes"
    retro_id = Column(Integer, ForeignKey("retros.retro_id"), nullable=False)
    note_id = Column(Integer, ForeignKey("notes.note_id"), nullable=False)

    def __init__(self, retro_id, note_id):
        self.retro_id = retro_id
        self.note_id = note_id