from fastapi import FastAPI 
from pydantic import BaseModel
from typing import Optional
#uvicorn main:app --reload

app=FastAPI()

class Post(BaseModel):
    title:str
    content:str
    publish:bool=True
    rating:Optional[int]=None


@app.get("/")
def root():
    return {"message":"hello world"}

@app.get("/posts")
def get_posts():
    return {"data":'this is your post'}

@app.post('/posts')
def create_posts(post:Post): 
    print(post.model_dump())
    return {"data":post}



