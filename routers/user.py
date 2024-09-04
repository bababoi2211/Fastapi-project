

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter


from sqlalchemy.orm import Session

from routers import oauth2
from database import engine, get_db
import models
import schema
import utils


# connection
models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/users"
)

# for this method we cant use Schema Becuse of the validating email that Already Exist


@router.post("/",  status_code=status.HTTP_201_CREATED)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

    users = db.query(models.User.email).all()
    print(users)
    print(type(users))
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    print(users)
    # print(type(new_user))
    for i in users:
        if new_user.email in i:
            return {"Error": "This User Exist In The DataBase Please Choose Another One "}

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "ID": new_user.id,
        "STORE NAME": new_user.store_name,
        "EMAIL": new_user.email,
        "CREATED_AT": new_user.created_at
    }


@router.get("/{id}", response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db), user_cred: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the user with the id of {id} doesnt Exist")
    return user.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), user_cred: int = Depends(oauth2.get_current_user)):

    target_user = db.query(models.User).filter(models.User.id == id)
    print(target_user)

    if target_user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the user with the id of {id} doesnt Exist")

    target_user.delete(synchronize_session=False)
    db.commit()
