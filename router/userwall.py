from schemas import PostBase, PostDisplay, UserAuth, UserBase
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_post
from auth.oauth2 import oauth2_scheme
from typing import List
from auth.oauth2 import get_current_user
from datetime import datetime
import os
import uuid

router = APIRouter(
    tags=['userwall']
)

# This is used to post an image to the user DB images
@router.post("/posts/")
def create_post(content: str, creator_id: int, username: str, image: UploadFile = File(None), db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    image_url = None
    if image:
        if not is_valid_image(image.filename):
            raise HTTPException(status_code=400, detail="Only JPG, JPEG, PNG and GIF images are allowed.")
        image_url = save_image(image)
    
    new_post = db_post.create_post(db=db, request=PostBase(content=content, creator_id=creator_id, username=username, image_url=image_url, timestamp=datetime.now()))
    return new_post

# This endpoint is used to retrieve posts # Get all posts from User 
@router.get("/posts/all")
def posts(db: Session = Depends(get_db)):
    posts = db_post.get_all(db)
    return posts

# Function to save uploaded image
def save_image(image: UploadFile):
    unique_filename = str(uuid.uuid4()) + os.path.splitext(image.filename)[-1]
    file_path = os.path.join("images", unique_filename)
    with open(file_path, "wb") as f:
        f.write(image.file.read())
    return file_path

# Function to check if the file type is valid
def is_valid_image(filename: str) -> bool:
    valid_extensions = ('.jpg', '.jpeg', '.png', '.gif')
    ext = os.path.splitext(filename)[-1].lower()
    return ext in valid_extensions

#get spesific post
@router.get('/posts/{id}') #, response_model=PostDisplay)
def get_post(id:int, db:Session = Depends(get_db)): #secure end-point #token: str = Depends(oauth2_scheme)
    return {
        'data': db_post.get_post(db,id)
    }

#Update User
@router.put('/posts/{id}')
def update_post(id: int, request:PostBase, db:Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_post.update_post(db, id, request)

#Delete Post
@router.delete('/posts/{id}')
def delete_post(id:int, db:Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_post.delete_post(db, id)





