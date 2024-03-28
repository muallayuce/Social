from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, DateTime
from sqlalchemy import TIMESTAMP, Column, Table, Text
from .database import Base


# Define the association table for many-to-many relationship
group_membership = Table( 
    'group_membership', Base.metadata,
    Column('membership_id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('username', String),
    Column('group_id', Integer, ForeignKey('groups.id'))
)


class DbUser(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

    # Explicitly define the foreign key relationship for friendships
    friendships = relationship("DbFriendship", back_populates="user", foreign_keys="[DbFriendship.user_id]")

    posts = relationship('DbPost', back_populates='user')

    # Many-to-Many relationship with groups
    groups = relationship("DbGroup", secondary=group_membership, back_populates="members")

    # One-to-Many relationship with group posts
    group_posts = relationship('DbGroupPost', back_populates='author')


class DbFriendship(Base):
    __tablename__ = 'friendships'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    friend_id = Column(Integer, ForeignKey('users.id'))
    accepted = Column(Boolean, default=False)  # New field to indicate acceptance status

    user = relationship("DbUser", foreign_keys=[user_id], back_populates="friendships")
    friend = relationship("DbUser", foreign_keys=[friend_id], back_populates="friendships")
    

class DbPost(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    content = Column(String)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    username = Column(String)
    image_url = Column(String)

    user = relationship('DbUser', back_populates='posts')
    comments = relationship('DbComment', back_populates= 'post')


class DbComment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    username = Column(String)
    timestamp = Column(DateTime)
    post_id = Column(Integer, ForeignKey('posts.id'))
    
    post = relationship('DbPost', back_populates= 'comments')


class DbGroup(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime)
    creator_id = Column(Integer, ForeignKey('users.id'))  
    is_public = Column(Boolean, default=True)
    visibility = Column(String, default="public")

    # One-to-Many relationship with group posts
    group_posts = relationship('DbGroupPost', back_populates='group')

    # Define the 'members' attribute
    members = relationship("DbUser", secondary=group_membership, back_populates="groups")


class DbGroupPost(Base):
    __tablename__ = 'group_posts'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    created_at = Column(DateTime)
    

    author = relationship('DbUser', back_populates='group_posts')  # Many-to-One relationship with user
    group = relationship('DbGroup', back_populates='group_posts')





