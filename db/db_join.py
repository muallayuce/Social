from sqlalchemy.orm import Session
from db.database import Base

# Define the association table for many-to-many relationship
group_membership = Base.metadata.tables['group_membership']

# Add a user to a group
def join_group(db: Session, group_membership_table, group_id: int, user_id: int, username: str, membership_id: int):
    db.execute(group_membership_table.insert().values(group_id=group_id, user_id=user_id, username=username, membership_id=membership_id))
    db.commit()
