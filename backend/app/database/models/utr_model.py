from sqlalchemy import Column, Integer, String, ForeignKey

from .. import Base

class UserToRetro(Base):
    __tablename__ = "user_to_retro"
    utr_id = Column(Integer, primary_key=True, autoincrement= "auto", nullable=False)
    user_id = Column(String, nullable=False)
    retro_id = Column(Integer, ForeignKey("retros.retro_id"), nullable=False)

    def __init__(self, user_id, retro_id):
        self.user_id = user_id
        self.retro_id = retro_id