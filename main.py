from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

app = FastAPI()

SQLALCHEMY_DATABASE_URL = 'mysql+mysqlconnector://root:root@localhost:3306/prova'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Post(Base):
    __tablename__ = "post"
    
    PostID = Column(Integer, primary_key=True, index=True)
    Title = Column(String(50), nullable=False)
    Created = Column(String(50), nullable=False)
    Text = Column(String(100), nullable=False)

class Comment(Base):
    __tablename__ = "comment"
    
    CommentID = Column(Integer, primary_key=True, index=True)
    PostID = Column(Integer, ForeignKey('post.PostID', ondelete='CASCADE'), nullable=False)
    Text = Column(String(100), nullable=False)
    Created = Column(String(50), nullable=False)
    User = Column(String(50), nullable=False)

class AttachedFiles(Base):
    __tablename__ = "attachedfiles"
    
    AttatchedFilesID = Column(Integer, primary_key=True, index=True)
    CommentID = Column(Integer, ForeignKey('comment.CommentID', ondelete='CASCADE'), nullable=False)
    Title = Column(String(50), nullable=False)
    Created = Column(String(50), nullable=False)
    FilePath = Column(String(100), nullable=False)

Base.metadata.create_all(bind=engine)

@app.post("/posts/")
def create_post(title: str, text: str):
    created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    post = Post(Title=title, Created=created_time, Text=text)
    db = SessionLocal()
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@app.get("/posts/{post_id}")
def read_post(post_id: int):
    db = SessionLocal()
    post = db.query(Post).filter(Post.PostID == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.post("/comments/")
def create_comment(post_id: int, text: str, user: str):
    created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db = SessionLocal()
    post = db.query(Post).filter(Post.PostID == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    comment = Comment(PostID=post_id, Text=text, Created=created_time, User=user)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

@app.post("/files/")
def create_attached_files(comment_id: int, title: str, file_path: str):
    created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db = SessionLocal()
    comment = db.query(Comment).filter(Comment.CommentID == comment_id).first()
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    attached_file = AttachedFiles(CommentID=comment_id, Title=title, Created=created_time, FilePath=file_path)
    db.add(attached_file)
    db.commit()
    db.refresh(attached_file)
    return attached_file
