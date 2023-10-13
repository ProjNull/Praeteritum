from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Users(Base):
    __tablename__ = "UsersModel"

    User_ID = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    Name = Column(String, nullable=False)
    Email = Column(String, nullable=False)
    Password = Column(String, nullable=False)
    Description = Column(String, nullable=True)

class Permissions(Base):
    __tablename__ = "PermissionsModel"

    Permission_ID = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    Permission_level = Column(Integer, nullable=False, default=0)
    User_ID = Column(Integer, ForeignKey('UsersModel.User_ID'), nullable=False)
    Group_ID = Column(Integer, ForeignKey('GroupsModel.Group_ID'), nullable=False, unique=False, primary_key=False)

class Groups(Base):
    __tablename__ = "GroupsModel"

    Group_ID = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    Name = Column(String, nullable=False)
    Description = Column(String, nullable=True)

#class Boards(Base):
#    __tablename__ = "BoardsrModel"
#
#    Name = Column(String, nullable=False)
#    uID = Column(Integer, nullable=False, unique=True, primary_key=True)
#    Description = Column(String, nullable=True)
#
#class Questions(Base):
#    __tablename__ = "QuestionsModel"
#
#    uID = Column(Integer, nullable=False, unique=True, primary_key=True)
#    Description = Column(String, nullable=True)
#
#class Feedback(Base):
#    __tablename__ = "FeedbackModel"
#
#    uID = Column(Integer, nullable=False, unique=True, primary_key=True)
#
#class Reaction(Base):
#    __tablename__ = "ReactionModel"
#
#    uID = Column(Integer, nullable=False, unique=True, primary_key=True)