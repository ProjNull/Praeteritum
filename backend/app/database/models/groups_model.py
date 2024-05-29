from sqlalchemy import Column, Integer, String

from .. import Base

class Groups(Base):
    __tablename__ = "groups"
    group_id = Column(Integer, primary_key=True, autoincrement= "auto", nullable=False)
    name = Column(String(64), nullable=False)

    def __init__(self, name):
        self.name = name