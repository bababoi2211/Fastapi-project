
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import schema
import models
from database import get_db
from . import oauth2

router = APIRouter(
    prefix="/vote",
    tags=['VOTE']
)


@router.post("/")
def vote(vote: schema.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_exist = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"This post with the ID Of {vote.post_id } Doesnt Exist!!")

    
    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)

    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"the user with the id {current_user.id} has already voted on post {vote.post_id}")

        new_vote = models.Votes(post_id=vote.post_id, user_id=current_user.id)

        db.add(new_vote)
        db.commit()
        return {"message": "Succesfuly voted"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                 detail=f"The Vote doesnt Exist To Be Deleted!")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Succesfuly deleted vote"}
