from fastapi import FastAPI ,Response,status,HTTPException,Depends
from pydantic import BaseModel
from typing import Optional
from . import models
from .database import engine,get_db
from sqlalchemy.orm import  session
#uvicorn main:app --reload


models.Base.metadata.create_all(bind=engine)

app=FastAPI()







class Post(BaseModel):
    title:str
    content:str
    publish:bool=True
    rating:Optional[int]=None

myPost=[{"id":1,"title":"this is title 1","content":"content 1 "},{"id":2,"title":"title 2 ","content":"content 2 is here"}]

def find_post(id):
    for p in myPost:
        if p['id']==id:
            print(p)
            return p
    


@app.get("/")
def root():
    return {"message":"hello world"}

@app.get("/sqlalchemy")
def test_posts(db:session=Depends(get_db)):
    posts=db.query(models.Post).all()
    return {"response":posts}


@app.get("/posts")
def get_posts():
    return {"data":myPost}


@app.post('/posts',status_code=status.HTTP_201_CREATED)
def create_posts(post:Post): 
    myPost.append(post.model_dump())
    print(myPost)
    return {"data":myPost} 

@app.get('/posts/latest')
def get_latest():
    post=myPost[-1]
    return {"latest_post":post}

@app.get('/posts/{id}')
def get_post(id:int,response:Response):
    post = find_post(id)
    if not post:
        response.status_code=status.HTTP_404_NOT_FOUND 
    return {"post_detail":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    for i in myPost:
        if i["id"]==id:
            print("---------------------------",)
            myPost.remove(i)
    print(myPost)
    return {"data":myPost}


