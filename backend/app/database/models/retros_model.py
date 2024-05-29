from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, ARRAY

from .. import Base

class Retros(Base):
    __tablename__ = "retros"
    retro_id = Column(Integer, primary_key=True, autoincrement= "auto", nullable=False)
    group_id = Column(Integer, ForeignKey("groups.group_id"), nullable=False)
    user_id = Column(String, nullable=False)
    name = Column(String(64), nullable=False)
    stage = Column(Integer, default=0)
    ended = Column(Boolean, default=False)

    def __init__(self, group_id, user_id, name):
        self.group_id = group_id
        self.user_id = user_id
        self.name = name