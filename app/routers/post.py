from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from app import schemas, models, oauth2
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)
              , limit: int = 10
              , offset: int = 0
              , search: Optional[str] = ""):

    return db.query(models.Post) \
        .filter(models.Post.title.contains(search)) \
        .order_by(models.Post.created_at) \
        .limit(limit).offset(offset).all()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(
        post: schemas.PostCreate,
        db: Session = Depends(get_db), 
        current_user: schemas.UserResponse = Depends(oauth2.get_current_user)
    ):
    my_post = models.Post(user_id = current_user.id, **post.dict())
    db.add(my_post)
    db.commit()
    db.refresh(my_post)
    return my_post


@router.get("/{id:int}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db),
             current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == str(id)).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with {id=} was not found')

    return post


@router.delete("/{id:int}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == str(id))
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id=} was not found.")
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Not authorize to perform requested action.')

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id:int}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post(
        id: int, 
        updated_post: schemas.PostCreate, 
        db: Session = Depends(get_db),
        current_user: schemas.UserResponse = Depends(oauth2.get_current_user)
    ):

    post_query = db.query(models.Post).filter(models.Post.id == str(id))
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with {id=} was not found.')
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Not authorize to perform requested action.')

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
