from sqlalchemy import Column, Integer, String, ForeignKey
from enum import Enum

from .. import Base
from .groups_model import Groups


class TeamPermissionLevel(Enum):
    """Represents a member's permissions in a team
    0 (Guest): Means the user is not part of the team
    1 (Member): Means the user can join the team's retros
    2 (Manager): Means the user can create and manage retros that the team owns and can add others into the team
    3 (Admin): Same as manager, but can promote others to manager and delete the team
    """

    GUEST = 0
    MEMBER = 1
    MANAGER = 2
    ADMIN = 3


class TeamModel(Base):
    __tablename__ = "teams"
    team_id: int = Column(
        Integer, primary_key=True, autoincrement="auto", nullable=False
    )
    group_id: int = Column(Integer, ForeignKey("groups.group_id"), nullable=False)
    name: str = Column(String, nullable=False)

    def __init__(self, group_id: int, name: str):
        self.group_id = group_id
        self.name = name


class UserToTeamModel(Base):
    __tablename__ = "user_to_team"
    utt_id: int = Column(
        Integer, primary_key=True, autoincrement="auto", nullable=False
    )
    team_id: int = Column(Integer, ForeignKey("teams.team_id"), nullable=False)
    user_id: str = Column(String, nullable=False)
    permission_level: int = Column(Integer, nullable=False, default=1)

    def __init__(self, team_id, user_id):
        self.team_id = team_id
        self.user_id = user_id

    def set_permission_level(self, permission_level: TeamPermissionLevel):
        """! THIS DOESN'T COMMIT THE CHANGES

        Args:
            permission_level (TeamPermissionLevel): The new permission level
        """
        self.permission_level = permission_level.value
