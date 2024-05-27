from sqlalchemy import Column, Integer

from .. import Base


class SusModel(Base):
    __tablename__ = "sus"
    sus_id: int = Column(Integer, primary_key=True)

    def __init__(self, sus_id: int):
        self.sus_id = sus_id
