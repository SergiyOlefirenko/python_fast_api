from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from . import schemas 
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/sqlalchemy")
def test_sqlalchemy(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/")
async def root():
    return {"message": "Hellow world!"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    return {"data": db.query(models.Post).all()}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    my_post = models.Post(**post.dict())
    db.add(my_post)
    db.commit()
    db.refresh(my_post)
    return {"data": my_post}

@app.get("/posts/{id:int}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == str(id)).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with {id=} was not found')

    return {"post_detail": post}

@app.delete("/posts/{id:int}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == str(id))

    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id=} was not found.")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id:int}", status_code=status.HTTP_200_OK)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == str(id))
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with {id=} was not found.')

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return {'data': post_query.first()}