from fastapi import HTTPException
from ..models.retros_model import Retros as RetroModel
from ..models.utr_model import UserToRetro as UTRModel
from .. import Session
from .schemas import retro_schemas


async def create_retro(db: Session, query: retro_schemas.RetroCreate):
    retro = RetroModel(
        query.organization_id,
        query.user_id,
        query.name,
        query.description,
        query.is_public,
    )
    db.add(
            retro
        )


async def get_retro_by_id(db: Session, query: retro_schemas.QueryRetro):
    return db.query(
            RetroModel
        ).filter(
                RetroModel.retro_id == query.retro_id
            ).first()


async def get_all_retros_in_org(
    db: Session, query: retro_schemas.QueryAllRetrosInOrganization
):
    return (
        db.query(
                RetroModel
            )
            .filter(
                    RetroModel.group_id == query.organization_id
                )
            .all()
        )


async def get_all_retros_by_user(db: Session, query: retro_schemas.QueryAllRetrosForUser):
    return db.query(RetroModel).filter(RetroModel.user_id == query.user_id).all()


async def fetch_retros(db: Session, query: retro_schemas.QueryRetroList):
    return (
        db.query(
                RetroModel
            )
            .filter(
                RetroModel.group_id == query.organization_id
                and (
                    False
                    if not query.match_Active
                    else RetroModel.is_active == query.is_active
                )
                and (
                        RetroModel.is_public if query.public_only else True
                    )
                )
                .all()
            )


async def delete_retro(db: Session, query: retro_schemas.QueryRetro):
    db.query(
            RetroModel
        ).filter(
                RetroModel.retro_id == query.retro_id
            ).delete()


async def update_retro(db: Session, query: retro_schemas.RetroUpdate):
    retro = get_retro_by_id(
        db, 
        retro_schemas.QueryRetro(
                retro_id=query.retro_id
            )
        )
    if query.name:
        retro.name = query.name
    if query.description:
        retro.description = query.description
    if query.is_public is not None:
        retro.is_public = query.is_public
    if query.stage is not None:
        retro.stage = query.stage
    if query.is_active is not None:
        retro.is_active = query.is_active
    db.add(retro)


async def get_retro_members(db: Session, query: retro_schemas.QueryRetro):
    return db.query(UTRModel).filter(UTRModel.retro_id == query.retro_id).first()


async def add_user_to_retro(db: Session, query: retro_schemas.UserToRetro):
    retro = await get_retro_by_id(
        db, 
        retro_schemas.QueryRetro(
                retro_id=query.retro_id
            )
        )
    
    db.add(
        UTRModel(
                retro_id=retro.retro_id, 
                user_id=query.user_id
            )
        )


async def remove_user_from_retro(db: Session, query: retro_schemas.UserToRetro):
    db.query(
            UTRModel
        ).filter(
                UTRModel.retro_id == query.retro_id, 
                UTRModel.user_id == query.user_id
            ).delete()
