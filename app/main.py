# pylint: disable=broad-except

from random import randrange
from typing import Optional
import time

import psycopg2
from fastapi import FastAPI, HTTPException, Response, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="postgres",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as e:
        print("Connection to database failed")
        print(e)
        time.sleep(3)


my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite foods", "content": "I like pizza", "id": 2},
]


def find_post(post_id):
    for post in my_posts:
        if post["id"] == post_id:
            return post
    return None


def find_index_post(post_id):
    for i, post in enumerate(my_posts):
        if post["id"] == post_id:
            return i
    return None


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """ INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(post_id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} was not found",
        )
    return {"post_detail": post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(post_id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} does not exist",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    index = find_index_post(post_id)

    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} does not exist",
        )

    post_dict = post.dict()
    post_dict["id"] = post_id
    my_posts[index] = post_dict
    return {"data": post_dict}
