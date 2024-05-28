from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from .. import Base

class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement= "auto", nullable=False)
    displayname = Column(String(64), nullable=False)
    usermane = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)


    def __init__(self, displayname, usermane, email, password):
        self.displayname = displayname
        self.usermane = usermane
        self.email = email
        self.password = password

class UserToGroup(Base):
    __tablename__ = "user_to_group"
    utg_id = Column(Integer, primary_key=True, autoincrement= "auto", nullable=False)
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
    ended = Column(Boolean, nullable=False)


    def __init__(self, name, group_id):
        self.name = name
        self.group_id = group_id

class Actions(Base):
    __tablename__ = "actions"
    action_id = Column(Integer, primary_key=True, autoincrement= "auto", nullable=False)
    retro_id = Column(Integer, ForeignKey("retros.retro_id"), nullable=False)
    name = Column(String(64), nullable=False)
    description = Column(String(250), nullable=True)

    def __init__(self, retro_id, name, description):
        self.retro_id = retro_id
        self.name = name
        self.description = description