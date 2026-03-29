from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas,utils
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import get_db


router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=201, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return new_user

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not user with id {id} exists"
        )
    
    return user