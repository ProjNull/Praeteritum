from typing import List
from fastapi import HTTPException
from ..models.utg_model import UserToGroup
from ..models.retros_model import Retros
from ..models.utr_model import UserToRetro
from .. import Session
from .schemas import retro_schemas


def create_retro(db: Session, query: retro_schemas.RetroCreate, user_id: str):
    if db.query(UserToGroup.user_id).filter(UserToGroup.group_id==query.group_id and UserToGroup.user_id==user_id).first() is None:
        raise HTTPException("User is not in this group")
    
    retro = Retros(query.group_id, user_id, query.name, query.description, query.is_public,)
    db.add(retro)


def get_retro_by_id(db: Session, query: retro_schemas.GetRetro, user_id: str):
    retro = db.query(Retros).filter(Retros.retro_id == query.retro_id).first()
    if retro is None:
        raise HTTPException("Retro not found")
    
    relation = db.query(UserToGroup.permissions).filter(UserToGroup.group_id==retro.group_id and UserToGroup.user_id==user_id).first()
    access = db.query(UserToRetro.retro_id).filter(UserToRetro.user_id==user_id and UserToRetro.retro_id == retro.retro_id).first()
    if relation is None or access is None:
        raise HTTPException("User is not in this retro")
    
    return retro

def get_all_retros_in_group(db: Session, query: retro_schemas.GetAllRetrosInGroup, user_id: str):
    permissions = db.query(UserToGroup.permissions).filter(UserToGroup.group_id==query.group_id and UserToGroup.user_id==user_id).first()
    if permissions is None:
        raise HTTPException("User is not in this group")

    retros = db.query(Retros).join(UserToRetro, Retros.retro_id == UserToRetro.retro_id).filter(Retros.group_id == query.group_id and (UserToRetro.user_id == user_id or permissions > 1))
    if retros.first() is None:
        raise HTTPException("User does not have access to this retro")

    if query.filter.public_only:
        retros = retros.filter(Retros.is_public == True)
    if query.filter.is_active:
        retros = retros.filter(Retros.is_active == True)
    return retros.all()


        
def get_all_retros_for_user(db: Session, query: retro_schemas.FilterRetro, user_id: str):
    retros = db.query(Retros).join(UserToRetro, Retros.retro_id == UserToRetro.retro_id).filter(Retros.user_id == user_id or UserToRetro.user_id == user_id)
    if query.is_active:
        retros = retros.filter(Retros.is_active == True)
    if query.public_only:
        retros = retros.filter(Retros.is_public == True)
    return retros.all()

def delete_retro(db: Session, query: retro_schemas.DeleteRetro, user_id: str):
    retro = db.query(Retros).filter(Retros.retro_id == query.retro_id)
    if retro.first() is None:
        raise HTTPException("Retro not found")
    
    group_id = db.query(Retros.group_id).filter(Retros.retro_id == query.retro_id).first()
    isPermited = db.query(UserToGroup.permissions).filter(UserToGroup.user_id==user_id and UserToGroup.group_id == group_id).first() > 1
    isAuthor = db.query(Retros.user_id).filter(Retros.retro_id == query.retro_id).first() == user_id
    if not isPermited or not isAuthor:
        raise HTTPException("User is not permited to delete this retro")
    retro.delete()

def update_retro(db: Session, query: retro_schemas.UpdateRetro, user_id: str):
    retro = db.query(Retros).filter(Retros.retro_id == query.retro_id).first()
    if retro is None:
        raise HTTPException("Retro not found")
    
    isPermited = db.query(UserToGroup.permissions).filter(UserToGroup.user_id==user_id and UserToGroup.group_id == retro.group_id).first() > 1
    isAuthor = retro.user_id == user_id
    if not isPermited or not isAuthor:
        raise HTTPException("User is not permited to update this retro")

    if query.retro_id is not None: retro.retro_id = query.retro_id
    if query.name is not None: retro.name = query.name
    if query.description is not None: retro.desc = query.description
    if query.is_public is not None: retro.is_public = query.is_public
    if query.stage is not None: retro.stage = query.stage
    if query.is_active is not None: retro.is_active = query.is_active
    db.add(retro)

def get_retro_members(db: Session, query: retro_schemas.GetRetroMembers, user_id: str) -> List[str]:
    retro = db.query(Retros).filter(Retros.retro_id == query.retro_id).first()
    if retro is None:
        raise HTTPException("Retro not found")
    isPermited = db.query(UserToGroup.permissions).filter(UserToGroup.user_id==user_id and UserToGroup.group_id == retro.group_id).first() > 1
    isAsigned = db.query(UserToRetro.user_id).filter(UserToRetro.retro_id == query.retro_id, UserToRetro.user_id == user_id).first() is not None
    isAuthor = retro.user_id == user_id
    if not isPermited or not isAsigned or not isAuthor:
        raise HTTPException("User is not permited to get this retro members")
    return db.query(UserToRetro.user_id).filter(UserToRetro.retro_id == query.retro_id).all()

def add_user_to_retro(db: Session, query: retro_schemas.AddUserToRetro, user_id: str):
    retro = db.query(Retros).filter(Retros.retro_id == query.retro_id).first()
    if retro is None:
        raise HTTPException("Retro not found")
    
    isPermited = db.query(UserToGroup.permissions).filter(UserToGroup.user_id==user_id and UserToGroup.group_id == retro.group_id).first() > 1
    isAuthor = retro.user_id == user_id
    if not isPermited or not isAuthor:
        raise HTTPException("User is not permited to add user to this retro")
    
    db.add(UserToRetro(retro_id=retro.retro_id, user_id=query.user_id))

def remove_user_from_retro(db: Session, query: retro_schemas.RemoveUserFromRetro, user_id: str):
    retro = db.query(Retros).filter(Retros.retro_id == query.retro_id).first()
    if retro is None:
        raise HTTPException("Retro not found")
    
    isPermited = db.query(UserToGroup.permissions).filter(UserToGroup.user_id==user_id and UserToGroup.group_id == retro.group_id).first() > 1
    isAuthor = retro.user_id == user_id
    if not isPermited or not isAuthor:
        raise HTTPException("User is not permited to add user to this retro")
    
    db.query(UserToRetro).filter(UserToRetro.retro_id == query.retro_id, UserToRetro.user_id == query.user_id).delete()