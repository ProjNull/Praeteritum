from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = "UsersModel"

    User_ID = Column(
        Integer, nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    Name = Column(String, nullable=False)
    Email = Column(String, nullable=False)
    Password = Column(String, nullable=False)
    Description = Column(String, nullable=True)


class Permissions(Base):
    __tablename__ = "PermissionsModel"

    Permission_ID = Column(
        Integer, nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    Permission_Level = Column(Integer, nullable=False, default=0)
    User_ID = Column(Integer, ForeignKey("UsersModel.User_ID"), nullable=False)
    Group_ID = Column(Integer, ForeignKey(
        "GroupsModel.Group_ID"), nullable=False)


class Groups(Base):
    __tablename__ = "GroupsModel"

    Group_ID = Column(
        Integer, nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    Group_Name = Column(String, nullable=False)
    Description = Column(String, nullable=True)


class Boards(Base):
    __tablename__ = "BoardsrModel"

    Board_ID = Column(
        Integer, nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    BoardName = Column(String, nullable=False)
    Description = Column(String, nullable=True)
    Group_ID = Column(Integer, ForeignKey(
        "GroupsModel.Group_ID"), nullable=False)
    Phase = Column(Integer, nullable=False)
    RevealPosts = Column(Boolean, nullable=False)
    isLocked = Column(Boolean, nullable=False)
    isVotingLocked = Column(Boolean, nullable=False, default=False)


class Questions(Base):
    __tablename__ = "QuestionsModel"

    Questions_ID = Column(
        Integer, nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    Content = Column(String, nullable=False)
    Description = Column(String, nullable=True)
    Columns = Column(String, nullable=False)
    Board_ID = Column(Integer, ForeignKey(
        "BoardsrModel.Board_ID"), nullable=False)


class Feedback(Base):
    __tablename__ = "FeedbackModel"

    Feedback_ID = Column(
        Integer, nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    Content = Column(String, nullable=False)
    ColumnName = Column(String, nullable=False)
    Questions_ID = Column(
        Integer, ForeignKey("QuestionsModel.Questions_ID"), nullable=False
    )
    User_ID = Column(Integer, ForeignKey("UsersModel.User_ID"), nullable=False)


class Reaction(Base):
    __tablename__ = "ReactionModel"

    Reaction_ID = Column(
        Integer, nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    Reaction_value = Column(Boolean, nullable=True)
    Feedback_ID = Column(
        Integer, ForeignKey("FeedbackModel.Feedback_ID"), nullable=False
    )
    User_ID = Column(Integer, ForeignKey("UsersModel.User_ID"), nullable=False)
