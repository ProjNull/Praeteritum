from sqlalchemy import Column, Integer, String, ForeignKey

from .. import Base

class Invites(Base):
    __tablename__ = "invites"
    invite_id = Column(Integer, primary_key=True, autoincrement= "auto", nullable=False)
    user_id = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.group_id"), nullable=False)

    def __init__(self, user_id, group_id):
        self.user_id = user_id
        self.group_id = group_id