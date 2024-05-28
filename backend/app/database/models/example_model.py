from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, ARRAY

from .. import Base

class UserToGroup(Base):
    __tablename__ = "user_to_group"
    utg_id = Column(Integer, primary_key=True, autoincrement= "auto", nullable=False)
    permissions = Column(Integer, nullable=False)
    user_id = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.group_id"), nullable=False)

    def __init__(self, user_id, group_id):
        self.user_id = user_id
        self.group_id = group_id

class Groups(Base):
    __tablename__ = "groups"
    group_id = Column(Integer, primary_key=True, autoincrement= "auto", nullable=False)
    name = Column(String(64), nullable=False)

    def __init__(self, name):
        self.name = name

class Retros(Base):
    __tablename__ = "retros"
    retro_id = Column(Integer, primary_key=True, autoincrement= "auto", nullable=False)
    group_id = Column(Integer, ForeignKey("groups.group_id"), nullable=False)
    name = Column(String(64), nullable=False)
    stage = Column(Integer, default=0)
    ended = Column(Boolean, default=False)


    def __init__(self, name, group_id):
        self.name = name
        self.group_id = group_id

class Notes(Base):
    __tablename__ = "notes"
    note_id = Column(Integer, primary_key=True, autoincrement= "auto", nullable=False)
    user_id = Column(String, nullable=False)
    retro_id = Column(Integer, ForeignKey("retros.retro_id"), nullable=False)
    content = Column(String(250), nullable=False)
    column = Column(Integer, nullable=False)
    
    def __init__(self, user_id, retro_id, content, column):
        self.user_id = user_id
        self.retro_id = retro_id
        self.content = content
        self.column = column
        
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