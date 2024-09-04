

from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import List


from sqlalchemy.orm import Session

from database import engine, get_db
import models
import schema
import utils


# connection
models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.post("/users", response_model=schema.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    # print(type(new_user))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{id}", response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)

    if not user:
        if user.first() == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"the user with the id of {id} doesnt Exist")
    return user


@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):

    target_user = db.query(models.User).filter(models.User.id == id)
    print(target_user)

    if target_user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the user with the id of {id} doesnt Exist")

    target_user.delete(synchronize_session=False)
    db.commit()
