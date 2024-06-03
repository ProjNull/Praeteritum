from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, ARRAY
from sqlalchemy.orm import relationship

from .. import Base

class UserToAction(Base):
    __tablename__ = "user_to_action"
    uta_id = Column(Integer, primary_key=True, autoincrement= "auto", nullable=False)
    user_id = Column(String, nullable=False)
    action_id = Column(Integer, ForeignKey("actions.action_id"), nullable=False)

    actions = relationship("Actions", lazy="joined")

    def __init__(self, user_id, action_id):
        self.user_id = user_id
        self.action_id = action_id