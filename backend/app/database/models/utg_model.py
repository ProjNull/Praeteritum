from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, ARRAY

from .. import Base

class UserToGroup(Base):
    __tablename__ = "user_to_group"
    utg_id = Column(Integer, primary_key=True, autoincrement= "auto", nullable=False)
    permissions = Column(Integer, default=0)
    user_id = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.group_id"), nullable=False)

    def __init__(self, user_id, group_id, permissions: int | None):
        self.user_id = user_id
        self.group_id = group_id
        if permissions is not None:
            self.permissions = permissions
