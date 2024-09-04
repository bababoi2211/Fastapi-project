
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor

from database import engine,get_db
import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI()




class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:

    try:

        conn = psycopg2.connect(host="localhost", database="fastapi",
                                user="postgres", password='dani1383', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Data Base Connection Was Succesful")
        break
    except Exception as err:
        print("Data Base Connection Was A Failure")
        print("Error : ", err)


@app.get("/posts")
def get_data():
    cursor.execute("""select * from post""")
    post = cursor.fetchall()
    return {"data": post}


@app.get("/posts/{id}")
def get_one(id: int
            ):

    cursor.execute("""select * from post where id =(%s)""", (str(id),))

    target_post = cursor.fetchone()

    # in ravash baray error hay bala tar az 10
    # if id > 9:
    #     cursor.execute(f"""select * from post where id = {str(id)}""")

    #     target_post = cursor.fetchone()

    if not target_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with the id of {id} Doesnt Exist")

    return {"Data": target_post}


@app.post("/posts")
def create_post(post: Post):

    # cursor.execute("select * from post")
    # posts = cursor.fetchall()

    cursor.execute(""" insert into post(title,content,published) values(%s,%s,%s) RETURNING *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()

    # if new_post in posts:
    #     raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
    #                         detail="This Post Exist In the Data Base")

    return {"data": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: str):

    cursor.execute("""delete from post where id = %s returning *""", (str(id)))
    target_post = cursor.fetchone()
    conn.commit()

    if target_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with the id {id} Desnt Exist")

    
    return {"Data": target_post}


@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED)
def update_post(id: str, post: Post):
    cursor.execute("""update post set title = %s,content = %s,published = %s where id = %s returning *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with the id:{id} Doesnt Exist")


