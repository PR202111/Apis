
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from .. import oauth2
from typing import Optional

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/",response_model=list[schemas.PostOut])
def get_post(db:Session = Depends(get_db)
    ,current_user:models.User = Depends(oauth2.get_current_user)
    ,limit: int = 10,skip:int = 0,search:Optional[str]=""):
    print(limit)
    p = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    results = db.query(
    models.Post,
    func.count(models.Vote.user_id).label("votes")
    ).join(
        models.Vote,
        models.Vote.post_id == models.Post.id,
        isouter=True).group_by(models.Post.id).limit(limit).offset(skip).all()
    
    return results

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.PostBase,db:Session = Depends(get_db),current_user:models.User = Depends(oauth2.get_current_user)):
   
    
    new_post = models.Post(owner_id = current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,response:Response,db:Session = Depends(get_db)):
   

    p = db.query(
    models.Post,
    func.count(models.Vote.user_id).label("votes")
    ).join(
        models.Vote,
        models.Vote.post_id == models.Post.id,
        isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not p:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} Not Found"
        )
    return p

@router.delete("/{id}")
def delete_post(id:int,db:Session=Depends(get_db),current_user:models.User = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post with id:{id} found to delete"
        )
    
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"This post doenst belong to current user to modify"
        )
    
    post_query.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(id:int,updated_post:schemas.PostUpdate,db:Session=Depends(get_db),current_user:models.User = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    db_post = post_query.first()
    
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post with id:{id} found"
        )
    
    if db_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"This post doenst belong to current user to modify"
        )

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()