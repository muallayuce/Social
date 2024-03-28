#crud.py
from sqlalchemy.orm.session import Session
from db.models import DbPost
from schemas import PostBase
from fastapi import HTTPException, status
import datetime
from typing import List

def create_post(db: Session, request:PostBase):
    new_post = DbPost(
        content= request.content,
        user_id = request.creator_id,
        username= request.username,
        image_url = request.image_url,
        timestamp = datetime.datetime.now()
    ) 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_all(db: Session) -> List[DbPost]:
    posts = db.query(DbPost).all()
    return posts

def get_post(db: Session, id:int):
    post = db.query(DbPost).filter(DbPost.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail= f'Post with id {id} not found')  #stop the code running
    return post

def update_post(db: Session, id:int, request:PostBase): #this func is designed to update user information in the db based on the data provided in the "request" parameter.
    post = db.query(DbPost).filter(DbPost.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail= f'Post with id {id} not found')  
    post.update({
        DbPost.content: request.content
    })
    db.commit()
    return 'ok'

def delete_post(db:Session, id: int):
    post =  db.query(DbPost).filter(DbPost.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail= f'Post with id {id} not found') 
    db.delete(post)
    db.commit()
    return 'ok'


