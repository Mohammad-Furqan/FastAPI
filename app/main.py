from fastapi import FastAPI ,Response,status,HTTPException,Depends
from pydantic import BaseModel
from typing import Optional
from . import models
from .database import engine,get_db
from sqlalchemy.orm import session
#uvicorn main:app --reload


models.Base.metadata.create_all(bind=engine)

app=FastAPI()







class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    # created_at:

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
    print('-00000-----------------------')
    posts=db.query(models.Post).all() 
    print('000000000000000000000000post',posts)
    return {"response":posts}


@app.get("/posts")
def get_posts(db:session=Depends(get_db)):
    myPost = db.query(models.Post).all()
    return {"data":myPost}


@app.post('/posts',status_code=status.HTTP_201_CREATED)
def create_posts(post:Post,db:session=Depends(get_db)): 
    # myPost.append(post.model_dump())
    print('http post request data :=----------------',post.model_dump())
    # new_post = models.Post(title=post.title,content=post.content,published=post.publish)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data":new_post} 

@app.get('/posts/latest')
def get_latest():
    post=myPost[-1]
    return {"latest_post":post}

@app.get('/posts/{id}')
def get_post(id:int,response:Response,db:session=Depends(get_db)):
    post = find_post(id)
    post = db.query(models.Post).filter(models.Post.id==id).first()
    print('-------------------------post by id --',post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {id} not found')
    return {"post_detail":post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {id} not found')
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}',status_code=status.HTTP_202_ACCEPTED)
def update_post(id:int,post:Post,db:session=Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post_exist = post_query.first()
    if not post_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {id} not found')
    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()

    return {"data":post_query.first()}