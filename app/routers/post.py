from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from app import schemas, models, oauth2
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(
        post: schemas.PostCreate,
        db: Session = Depends(get_db), 
        current_user: int = Depends(oauth2.get_current_user)
    ):
    my_post = models.Post(**post.dict())
    db.add(my_post)
    db.commit()
    db.refresh(my_post)
    return my_post


@router.get("/{id:int}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    print(current_user)
    post = db.query(models.Post).filter(models.Post.id == str(id)).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with {id=} was not found')

    return post


@router.delete("/{id:int}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == str(id))

    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id=} was not found.")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id:int}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post(
        id: int, 
        updated_post: schemas.PostCreate, 
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
    ):

    post_query = db.query(models.Post).filter(models.Post.id == str(id))
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with {id=} was not found.')

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
