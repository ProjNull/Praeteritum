from sqlalchemy import Column, Integer, String, ForeignKey

from .. import Base

class Actions(Base):
    __tablename__ = "actions"
    action_id = Column(Integer, primary_key=True, autoincrement= "auto", nullable=False)
    retro_id = Column(Integer, ForeignKey("retros.retro_id"), nullable=False)
    name = Column(String(64), nullable=False)
    description = Column(String(250), default="")

    def __init__(self, retro_id, name, description):
        self.retro_id = retro_id
        self.name = name
        self.description = description