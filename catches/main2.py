
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import List
from random import randrange

from pydantic import BaseModel

from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor


from database import engine, get_db
import models
import schema

connection = models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/product", response_model=List[schema.PostBase])
def get_all(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    print(type(post))
    return post


@app.post("/product", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db)):
    # new_post = models.Post(name=post.name, price=post.price,inventory=post.inventory, inorder=post.inorder)

    new_post = models.Post(**post.dict())

    db.add(new_post)

    db.commit()

    db.refresh(new_post)

    return new_post


@app.get("/posts/{id}")
def get_one_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the Product  With the Id of {id} Doesnt Exist! ")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the Product  With the Id of {id} Doesnt Exist!")

    post.delete(synchronize_session=False)
    db.commit()


# @app.put("/posts/{id}")
# def update_post(id: int, updated_post: UpdatePost.extract_data, db: Session = Depends(get_db)):

#     targeted_post = db.query(models.Post).filter(models.Post.id == id)

#     targeted_post_ = targeted_post.first()

#     updated_post = UpdatePost.extract_data(targeted_post_)
#     print(updated_post)

#     if targeted_post.first() == None:

#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"the Product  With the Id of {id} Doesnt Exist!")

#     # targeted_post.update(updated_post.dict(), synchronize_session=False)
#     targeted_post.update(update_post, synchronize_session=False)

#     db.commit()

#     return {"data": update_post}

# @app.put("/posts/{id}")
# def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db)):

#     targeted_post = db.query(models.Post).filter(models.Post.id == id)

#     if targeted_post.first() == None:

#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"the Product  With the Id of {id} Doesnt Exist!")

#     # targeted_post.update(updated_post.dict(), synchronize_session=False)
#     targeted_post.update(updated_post.dict(), synchronize_session=False)

#     db.commit()

#     return updated_post

@app.put("/posts/{id}")
def update_post(id: int, updated_post:schema.UpdatePost , db: Session = Depends(get_db)):
    targeted_post = db.query(models.Post).filter(models.Post.id == id)

    current_post = targeted_post.first()

    result = schema.UpdatePost.extract_data(current_post)


    # # updated_post.dict().update(result)
    updated_post.dict()["name"] = result["name"]
    updated_post.dict()["price"] = result["price"]
    updated_post.dict()["inventory"] = result["inventory"]
    updated_post.dict()["inorder"] = result["inorder"]
    print(updated_post)
    if targeted_post.first() == None:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the Product  With the Id of {id} Doesnt Exist!")

    # targeted_post.update(updated_post.dict(), synchronize_session=False)
    targeted_post.update(updated_post.dict() , synchronize_session=False)
    db.commit()
    return updated_post
