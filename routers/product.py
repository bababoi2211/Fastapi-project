
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional


from sqlalchemy.orm import Session
import psycopg2
from sqlalchemy import func

from routers import oauth2
from database import engine, get_db
import models
import schema


connection = models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/product"
)


@router.get("/fetch_data")
def fetch_data():
    # fetch('http://127.0.0.1:8000/product/fetch_data').then(res => res.json()).then(console.log)
    return "Hellooooo"


@router.get("/{id}")
def get_one_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # region find one post
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the Product  With the Id of {id} Doesnt Exist! ")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested Action")
    # endregion

    return post


# @router.get("/", response_model=List[schema.VotesOut])
# @router.get("/", response_model=List[schema.PostOut])
@router.get("/", response_model=List[schema.PostCreate])
def get_all(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
            limit: int = 10, skip: int = 0, vote: int = 1, search: Optional[str] = ""):
    post_1 = db.query(models.Post).all()
    # region Post with query parameter
    post = db.query(models.Post).filter(
        models.Post.user_id == current_user.id)
    post_parameter = post.filter(
        models.Post.name.contains(search)).limit(limit).offset(skip)
    all_post = post_parameter.all()

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{current_user.store_name} Didnt register anything  the Database")
    # endregion

    # region counting votes

    result_votes_join = db.query(models.Votes.user_id, func.count(models.Votes.user_id).label("count")).join(
        models.User, models.User.id == models.Votes.user_id).group_by(models.Votes.user_id)

    result_post_join = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id ==
                                                                                                   models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.name.contains(search)).limit(limit).offset(skip).all()
    # mikhastim yek filter baray vote peida konim
    result_post_join = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id ==
                                                                                                   models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Votes.post_id == vote).limit(limit).offset(skip).all()
    # endregion
    return post_1
    return result_post_join


@router.get("/join/{id}", response_model=schema.PostOut)
def get_one_join(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_join = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id ==
                                                                                            models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post_join:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The Post with the id {id} Doesnt Exist!!")

    return post_join


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # new_post = models.Post(name=post.name, price=post.price,inventory=post.inventory, inorder=post.inorder)

    new_post = models.Post(user_id=current_user.id, **post.dict())

    db.add(new_post)

    db.commit()

    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the Product  With the Id of {id} Doesnt Exist!")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not Autherized To Perform Action!")

    post.delete(synchronize_session=False)
    db.commit()


@router.put("/{id}")
def update_post(id: int, updated_post: schema.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    targeted_post_query = db.query(models.Post).filter(models.Post.id == id)

    post = targeted_post_query.first()
    # current_post =   targeted_post.first()

    # result = schema.UpdatePost.extract_data(current_post)

    # # updated_post.dict().update(result)
    # updated_post.dict()["name"] = result["name"]
    # updated_post.dict()["price"] = result["price"]
    # updated_post.dict()["inventory"] = result["inventory"]
    # updated_post.dict()["inorder"] = result["inorder"]
    # print(updated_post)
    if targeted_post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the Product  With the Id of {id} Doesnt Exist!")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not Autherized To Perform Action!")

    # targeted_post.update(updated_post.dict(), synchronize_session=False)
    targeted_post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return updated_post
