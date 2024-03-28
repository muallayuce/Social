from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas import GroupMembershipRequest
from db.models import DbUser, DbGroup
from db import db_join
from db.models import group_membership

router = APIRouter(
    prefix='/groups',
    tags=['groups']
)

@router.post("/{group_id}/join_group")
def join_group_endpoint(group_id: int, request: GroupMembershipRequest, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.id == request.user_id).first()
    group = db.query(DbGroup).filter(DbGroup.id == group_id).first()
    if not user or not group:
        raise HTTPException(status_code=404, detail="User or group not found")
    if user in group.members:
        raise HTTPException(status_code=400, detail="User already in the group")
    db_join.join_group(db, group_membership, group_id=group_id, user_id=user.id, username=user.username, membership_id=None)
    group.members.append(user)  # Assuming group.members is a list
    # Commit changes to the database session
    return {"message": "User joined the group"}

@router.put("/{group_id}/leave_group")
def leave_group_endpoint(group_id: int, request: GroupMembershipRequest, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.id == request.user_id).first()
    group = db.query(DbGroup).filter(DbGroup.id == group_id).first()
    if not user or not group:
        raise HTTPException(status_code=404, detail="User or group not found")
    if user in group.members:
        group.members.remove(user)
        db.commit()  # Commit changes to the database session
    return {"message": "User left the group"}
