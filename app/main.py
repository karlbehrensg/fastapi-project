# pylint: disable=broad-except, invalid-name
import time

import psycopg2
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor

from . import models
from .database import engine
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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


app.include_router(post.router)
app.include_router(user.router)
