from sqlalchemy.orm.session import Session
from db.models import DbGroup
from datetime import datetime
from fastapi import HTTPException, status
from typing import List
from schemas import GroupBase, GroupDisplay

def create_group(db: Session, request: GroupBase):
    new_group = DbGroup(
        name=request.name,
        description=request.description,
        creator_id=request.creator_id,
        is_public=request.is_public,
        visibility=request.visibility,
        created_at=datetime.now()
    )
    
    new_group.members = []  # Assign empty list to members attribute
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group

def get_all_groups(db: Session) -> List[GroupDisplay]:
    groups = db.query(DbGroup).all()
    return groups

def get_group(db: Session, group_id: int) -> GroupDisplay:
    group = db.query(DbGroup).filter(DbGroup.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Group with id {group_id} not found'
        )
    return group

def update_group(db: Session, group_id: int, request: GroupBase):
    group = db.query(DbGroup).filter(DbGroup.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Group with id {group_id} not found'
        )
    # Update group attributes
    group.name = request.name
    group.description = request.description
    group.is_public = request.is_public
    group.visibility = request.visibility
    db.commit()
    return group  # Return the updated group


def delete_group(db: Session, group_id: int):
    # Fetch the group from the database
    group = db.query(DbGroup).filter(DbGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Group post with id {id} not found') 
    db.delete(group)
    db.commit()
    return 'ok'
