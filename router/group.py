from typing import List
from db.models import DbUser
from schemas import GroupBase, GroupDisplay
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_group
from auth.oauth2 import get_current_user, oauth2_scheme

router = APIRouter(
    prefix='/groups',
    tags=['groups']
)

@router.post("/", response_model=GroupDisplay)
def create_group(group: GroupBase, db: Session = Depends(get_db)):
    return db_group.create_group(db=db, request=group)

@router.get("/all", response_model=List[GroupDisplay])
def read_groups(db: Session = Depends(get_db)):
    groups = db_group.get_all_groups(db=db)
    group_displays = []
    for group in groups:
        # Extract user IDs from group.members
        member_ids = [member.id for member in group.members]
        group_display = GroupDisplay(
            id=group.id,
            name=group.name,
            description=group.description,
            created_at=group.created_at,
            creator_id=group.creator_id,
            members=member_ids,  # Populate members with user IDs
            visibility=group.visibility
        )
        group_displays.append(group_display)
    return group_displays

@router.get("/{group_id}", response_model=GroupDisplay)
def read_group(group_id: int, db: Session = Depends(get_db)):
    group = db_group.get_group(db=db, group_id=group_id)
    
    # Extract user IDs from group.members
    member_ids = [member.id for member in group.members]
    
    return GroupDisplay(
        id=group.id,
        name=group.name,
        description=group.description,
        created_at=group.created_at,
        creator_id=group.creator_id,
        members=member_ids,  # Pass only integer IDs
        visibility=group.visibility
    )

@router.put("/{group_id}", response_model=GroupDisplay) 
def update_group(group_id: int, group: GroupBase, db: Session = Depends(get_db)):
    return db_group.update_group(db=db, group_id=group_id, request=group)

@router.delete("/{group_id}", response_model=str)
def delete_group(group_id: int, db: Session = Depends(get_db), current_user: DbUser  = Depends(get_current_user)):
    return db_group.delete_group(db=db, group_id=group_id)
