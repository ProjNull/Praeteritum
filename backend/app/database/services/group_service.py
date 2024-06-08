from typing import List
from ..models.groups_model import Groups
from ..models.utg_model import UserToGroup
from ..models.invites_model import Invites
from .schemas import group_schemas
from .. import Session
from fastapi import HTTPException, status


async def invite_user(db: Session, query: group_schemas.InviteUser, user_id: str):
    is_permitted = db.query(
            UserToGroup
        ).filter(
            UserToGroup.user_id == user_id,
            UserToGroup.group_id == query.group_id
        ).first()
    
    is_invited = db.query(
            Invites
        ).filter(
            Invites.user_id == query.user_id,
            Invites.group_id == query.group_id
        ).first()
    
    in_group = db.query(
            UserToGroup
        ).filter(
            UserToGroup.user_id == query.user_id,
            UserToGroup.group_id == query.group_id
        ).first()
    
    # Sender not in group
    if is_permitted is None: raise HTTPException(
        detail="Sender is not in this group", 
        status_code=status.HTTP_403_FORBIDDEN
    )

    # Not permitted
    if is_permitted.permissions < 1: raise HTTPException(
        detail="Sender is not permited to invite users to this group", 
        status_code=status.HTTP_403_FORBIDDEN
    )
    # Already invited
    if is_invited is not None: raise HTTPException(
        detail="Invited user is already invited to this group", 
        status_code=status.HTTP_409_CONFLICT
    )
    # Already in group
    if in_group is not None: raise HTTPException(
        detail="Invited user is already in this group", 
        status_code=status.HTTP_409_CONFLICT
    )
    
    db.add(
        Invites(
            user_id=query.user_id, 
            group_id=query.group_id
        )
    )


async def join_group(db: Session, query: group_schemas.JoinGroup, user_id: str):
    invite = db.query(
            Invites
        ).filter(
            Invites.user_id == user_id,
            Invites.group_id == query.group_id
        )
    # Not invited
    if invite.first() is None: raise HTTPException(
        detail="User is not invited to this group", 
        status_code=status.HTTP_403_FORBIDDEN
    )
    
    db.add(
        UserToGroup(
            user_id, 
            query.group_id, 
            1
        )
    )
    
    invite.delete()

async def get_invites(db: Session, user_id: str):
    return db.query(
            Invites
        ).filter(
            Invites.user_id == user_id
        ).all()


async def leave_group(db: Session, query: group_schemas.LeaveGroup, user_id: str):
    relation = db.query(
            UserToGroup
        ).filter(
            UserToGroup.user_id == user_id and 
            UserToGroup.group_id == query.group_id
        ).first()
    
    # Can't leave > Is owner
    if relation.permissions == 4: 
        raise HTTPException(
            detail="User is owner of this group, so you can't leave this group, you must transfer ownership or delete it instead",
            status_code=status.HTTP_403_FORBIDDEN
        )
    
    db.query(
            UserToGroup
        ).filter(
            UserToGroup.utg_id == relation.utg_id
        ).delete()


async def remove_from_group(db: Session, query: group_schemas.RemoveFromGroup, user_id: str):
    relation = db.query(
            UserToGroup
        ).filter(
            UserToGroup.user_id == user_id and 
            UserToGroup.group_id == query.group_id
        ).first()
    
    relation2 = db.query(
            UserToGroup
        ).filter(
            UserToGroup.user_id == query.user_id and 
            UserToGroup.group_id==query.group_id
        ).first()
        
    # Invoker not in group
    if relation is None: raise HTTPException(detail="User is not in this group", status_code=status.HTTP_403_FORBIDDEN)
    # User to be kicked not in group
    if relation2 is None: raise HTTPException(detail="User to be kicked is not in this group", status_code=status.HTTP_403_FORBIDDEN)
    # Not permitted
    if relation.permissions < relation2.permissions: raise HTTPException(
        detail="User is not permited to remove this user from this group", 
        status_code=status.HTTP_403_FORBIDDEN
    )
    
    db.query(
            UserToGroup
        ).filter(
            UserToGroup.utg_id == relation2.utg_id
        ).delete()
    
    
async def create_group(db: Session, query: group_schemas.CreateGroup) -> Groups:
    group = Groups(
            name=query.name
        )
    db.add(group)
    return group

async def update_permissions(db: Session, query: group_schemas.UpdatePermissions, user_id: str):
    relation = db.query(UserToGroup).filter(UserToGroup.user_id==user_id and UserToGroup.group_id==query.group_id).first()

    if query.permissions >= relation.permissions: raise HTTPException(
            detail="User is not permited to update this user's permissions to a equal or higher level", 
            status_code=status.HTTP_403_FORBIDDEN
        )

    new_relation = UserToGroup(query.user_id, query.group_id, query.permissions)
    db.add(new_relation)

async def set_owner(db: Session, query: group_schemas.SetOwner):
    db.add(
        UserToGroup(
            user_id=query.user_id, 
            group_id=query.group_id, 
            permissions=4
        )
    )


async def delete_group(db: Session, query: group_schemas.DeleteGroup, user_id: str):
    is_owner = db.query(
            UserToGroup
        ).filter(
            UserToGroup.user_id == user_id and 
            UserToGroup.group_id == query.group_id
        ).first().permissions
        
    # Not owner
    if is_owner != 4: raise HTTPException(
        detail="User is not the owner of this group", 
        status_code=status.HTTP_403_FORBIDDEN
    )
    
    db.query(
            UserToGroup
        ).filter(
            UserToGroup.group_id == query.group_id
        ).delete()
    
    db.query(
            Groups
        ).filter(
            Groups.group_id == query.group_id
        ).delete()
    
async def get_groups(db: Session, user_id: str) -> List[Groups]:
    return db.query(
            Groups
        ).join(
            UserToGroup, 
            Groups.group_id == UserToGroup.group_id
        ).filter(
            UserToGroup.user_id == user_id
        ).all()


async def get_users_in_group(db: Session, query: group_schemas.GetUsersInGroup, user_id: str) -> List[str]:
    has_access = db.query(
            UserToGroup
        ).filter(
            UserToGroup.group_id == query.group_id and 
            UserToGroup.user_id == user_id
        ).first() 
    
    # No access
    if has_access is None: raise HTTPException(
        detail="User does not have access to this group", 
        status_code=status.HTTP_403_FORBIDDEN
    )
    
    return [
        id.user_id for id in db.query(
            UserToGroup
        ).filter(
            UserToGroup.group_id == query.group_id
        ).all()
    ]