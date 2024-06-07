from typing import List
from fastapi import HTTPException, status
from ..models.utg_model import UserToGroup
from ..models.retros_model import Retros
from ..models.utr_model import UserToRetro
from .. import Session
from .schemas import retro_schemas


async def create_retro(db: Session, query: retro_schemas.RetroCreate, user_id: str):
    relation = db.query(
            UserToGroup
        ).filter(
            UserToGroup.group_id == query.group_id and 
            UserToGroup.user_id == user_id
        ).first()
    
    if relation is None: raise HTTPException(detail="User is not in this group", status_code=status.HTTP_403_FORBIDDEN)
    if relation.permissions < 2: raise HTTPException(detail="User is not permited to create a retro in this group", status_code=status.HTTP_403_FORBIDDEN)

    retro = Retros(query.group_id, user_id, query.name, query.description, query.columns, query.display_type, query.is_public)
    db.add(retro)
    return retro


async def get_retro_by_id(db: Session, query: retro_schemas.GetRetro, user_id: str):
    retro = db.query(
            Retros
        ).filter(
            Retros.retro_id == query.retro_id
        ).first()
    isPermited = db.query(
            UserToGroup
        ).filter(
            UserToGroup.group_id == retro.group_id and 
            UserToGroup.user_id == user_id
        ).first().permissions > 1
        
    access = db.query(
            UserToRetro
        ).filter(
            UserToRetro.user_id == user_id and 
            UserToRetro.retro_id == retro.retro_id
        ).first()
    
    # Not found
    if retro is None: raise HTTPException(detail="Retro not found", status_code=status.HTTP_404_NOT_FOUND)
    # Not in retro
    if access is None:
        if isPermited is None:
            raise HTTPException(detail="User is not in this retro", status_code=status.HTTP_403_FORBIDDEN)
    
    return retro

async def get_all_retros_in_group(db: Session, query: retro_schemas.GetAllRetrosInGroup, user_id: str):
    relation = db.query(
            UserToGroup
        ).filter(
            UserToGroup.group_id == query.group_id and 
            UserToGroup.user_id == user_id
        ).first()
    retros = db.query(
            Retros
        ).join(
            UserToRetro, 
            Retros.retro_id == UserToRetro.retro_id, 
            isouter=True
        ).filter(
        Retros.group_id == query.group_id and 
            (
                UserToRetro.user_id == user_id or 
                relation.permissions > 1
            )
        )
    
    # Is in group
    if relation is None: raise HTTPException(detail="User is not in this group", status_code=status.HTTP_403_FORBIDDEN)
    # Not permitted
    if retros.first() is None and relation.permissions < 2: raise HTTPException(detail="User does not have access to this retro", status_code=status.HTTP_403_FORBIDDEN)

    if query.filter is not None:
        if query.filter.public_only:
            retros = retros.filter(Retros.is_public == True)
        if query.filter.is_active:
            retros = retros.filter(Retros.is_active == True)
    return retros.all()


        
async def get_all_retros_for_user(db: Session, query: retro_schemas.FilterRetro, user_id: str):
    retros = db.query(
            Retros
        ).join(
            UserToRetro, 
            Retros.retro_id == UserToRetro.retro_id, 
            isouter=True
        ).filter(
            Retros.user_id == user_id or 
            UserToRetro.user_id == user_id
        )
    
    if query is not None:
        if query.is_active:
            retros = retros.filter(Retros.is_active == True)
        if query.public_only:
            retros = retros.filter(Retros.is_public == True)
    
    return retros.all()


async def delete_retro(db: Session, query: retro_schemas.DeleteRetro, user_id: str):
    retro = db.query(
            Retros
        ).filter(
            Retros.retro_id == query.retro_id
        )
        
    group_id = db.query(
            Retros
        ).filter(
            Retros.retro_id == query.retro_id
        ).first().group_id
        
    isPermited = db.query(
            UserToGroup
        ).filter(
            UserToGroup.user_id == user_id and 
            UserToGroup.group_id == group_id
        ).first().permissions > 1
    
    isAuthor = db.query(
            Retros
        ).filter(
            Retros.retro_id == query.retro_id
        ).first().user_id == user_id
    
    # Not found
    if retro.first() is None: raise HTTPException(detail="Retro not found", status_code=status.HTTP_403_FORBIDDEN)
    # Not permitted
    if not isPermited:
        if not isAuthor:
            raise HTTPException(detail="User is not permited to delete this retro", status_code=status.HTTP_403_FORBIDDEN)
    
    retro.delete()


async def update_retro(db: Session, query: retro_schemas.UpdateRetro, user_id: str):
    retro = db.query(
            Retros
        ).filter(
            Retros.retro_id == query.retro_id
        ).first()
        
    is_permited = db.query(
            UserToGroup
        ).filter(
            UserToGroup.user_id == user_id and 
            UserToGroup.group_id == retro.group_id
        ).first().permissions > 1
    
    is_author = retro.user_id == user_id
    
    # Not found
    if retro is None: raise HTTPException(detail="Retro not found", status_code=status.HTTP_404_NOT_FOUND)
    # Not permitted
    if not is_permited or not is_author: raise HTTPException(detail="User is not permited to update this retro", status_code=status.HTTP_403_FORBIDDEN)

    # Spaghetti
    if query.name is not None: retro.name = query.name
    if query.description is not None: retro.desc = query.description
    if query.is_public is not None: retro.is_public = query.is_public
    if query.stage is not None: retro.stage = query.stage
    if query.is_active is not None: retro.is_active = query.is_active
    
    db.add(retro)


async def get_retro_members(db: Session, query: retro_schemas.GetRetroMembers, user_id: str) -> List[str]:
    retro = db.query(
            Retros
        ).filter(
            Retros.retro_id == query.retro_id
        ).first()
        
    is_permited = db.query(
            UserToGroup
        ).filter(
            UserToGroup.user_id == user_id and 
            UserToGroup.group_id == retro.group_id
        ).first().permissions > 1
        
    is_asigned = db.query(
            UserToRetro
        ).filter(
            UserToRetro.retro_id == query.retro_id, 
            UserToRetro.user_id == user_id
        ).first() is not None
        
    is_author = retro.user_id == user_id
    
    # Not found
    if retro is None: raise HTTPException(detail="Retro not found", status_code=status.HTTP_403_FORBIDDEN)
    # Not permitted
    if not is_asigned: 
        if not is_permited:
            if not is_author:
                raise HTTPException(detail="User is not permited to get this retro members", status_code=status.HTTP_403_FORBIDDEN)
    
    return [i.user_id for i in db.query(
            UserToRetro
        ).filter(
            UserToRetro.retro_id == query.retro_id
        ).all()
    ]

async def add_user_to_retro(db: Session, query: retro_schemas.AddUserToRetro, user_id: str):
    retro = db.query(
            Retros
        ).filter(
            Retros.retro_id == query.retro_id
        ).first()
        
    is_permited = db.query(
            UserToGroup
        ).filter(
            UserToGroup.user_id == user_id and 
            UserToGroup.group_id == retro.group_id
        ).first().permissions > 1
    is_author = retro.user_id == user_id
    
    # Not found
    if retro is None: raise HTTPException(detail="Retro not found", status_code=status.HTTP_404_NOT_FOUND)
    # Not permitted
    if not is_permited or not is_author: raise HTTPException(detail="User is not permited to add user to this retro", status_code=status.HTTP_403_FORBIDDEN)
    
    db.add(
        UserToRetro(
            retro_id=retro.retro_id, 
            user_id=query.user_id
        )
    )


async def remove_user_from_retro(db: Session, query: retro_schemas.RemoveUserFromRetro, user_id: str):
    retro = db.query(
            Retros
        ).filter(
            Retros.retro_id == query.retro_id
        ).first()
        
    is_permited = db.query(
            UserToGroup
        ).filter(
            UserToGroup.user_id == user_id and 
            UserToGroup.group_id == retro.group_id
        ).first().permissions > 1
    
    is_author = retro.user_id == user_id
    
    if retro is None: raise HTTPException(detail="Retro not found", status_code=status.HTTP_404_NOT_FOUND)
    if not is_permited or not is_author: raise HTTPException(detail="User is not permited to add user to this retro", status_code=status.HTTP_403_FORBIDDEN)
    
    db.query(
            UserToRetro
        ).filter(
            UserToRetro.retro_id == query.retro_id, 
            UserToRetro.user_id == query.user_id
        ).delete()