from typing import List, Dict, Any, Optional
from pydantic import BaseModel, EmailStr, ValidationError, validator #data validation = pydantic = class
import re
from datetime import datetime

from db.models import DbUser

#Article inside UserDisplay
class Post(BaseModel):
    content: str
    class Config():
        from_attributes = True #orm_mode is changed to from_attributes

class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[^\w\s]', v):
            raise ValueError('Password must contain at least one special character')
        return v

class UserDisplay(BaseModel):
    username: str
    email: str
    items: List[Post] = []  #tpye of data which we want return
    class Config():
        from_attributes = True


class FriendshipBase(BaseModel):
    user_id: int
    friend_id: int

class FriendshipCreate(FriendshipBase):
    pass

class Friendship(FriendshipBase):
    id: int

    class Config:
        from_attributes = True

class FriendRequests(BaseModel):
    friend_requests: List[Friendship]
        

#user inside article display
class User(BaseModel):
    id:int
    username: str
    class Config():
        from_attributes = True

class PostBase(BaseModel): #what we recieve from the user when we are creating article
    content: str
    creator_id : int
    username: str
    image_url: Optional[str] = None
    timestamp: datetime

class  PostDisplay(BaseModel): #a data structure to send to the user when we are creating article
    content: str
    user: User
    timestamp: datetime
    image_url: Optional[str] = None
    class Config(): #convert instances of ORM models(db models) into dictionaries whrn serializing the data.
        from_attributes = True

class UserAuth(BaseModel):
    id: int
    username: str
    email: str


#For Post Display
class CommentDisplay(BaseModel):
    txt: str
    username: str
    timestamp: datetime
    class Config(): #convert instances of ORM models(db models) into dictionaries whrn serializing the data.
        from_attributes = True
    
class CommentBase(BaseModel):
    username: str
    txt: str
    post_id: int


#Group
        
class GroupBase(BaseModel):
    id: int  # Unique identifier for the group
    name: str
    description: str
    created_at: datetime = datetime.now()
    creator_id: int  # ID of the user who created the group
    members: List[int] = []  # List of user IDs representing members of the group
    is_public: bool = True  # Indicates whether the group is public or private
    visibility: str = "public"  # Visibility settings of the group
    #join_requests: List[int] = []  # List of user IDs who requested to join the group
    #avatar_url: str = None  # URL to the group's avatar or image
    #settings: Dict[str, Any] = {}  # Additional settings specific to the group
    #activities: List[str] = []  # Activities or events associated with the group

class GroupDisplay(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    creator_id: int
    members: List[int]
    visibility: str

    class Config:
        from_attributes = True

class GroupMembershipRequest(BaseModel):
    user_id: int
    username: str

class GroupMembershipResponse(BaseModel):
    message: str

class GroupPostBase(BaseModel):
    id: int
    content: str
    group_id: int
    author_id: int
    created_at: datetime = datetime.now()

class GroupPostCreate(GroupPostBase):
    pass

class GroupPostDisplay(BaseModel):
    content: str
    group_id: int
    author_id: int
    created_at: datetime = datetime.now()

    class Config:
        from_attributes = True

class GroupPostUpdate(BaseModel):
    content: str
