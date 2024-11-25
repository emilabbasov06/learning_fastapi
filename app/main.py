import psycopg
import time
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from psycopg.rows import dict_row

app = FastAPI()


class Post(BaseModel):
  title: str
  content: str
  published: bool = True
  rating: Optional[int] = None


while True:
  try:
    conn = psycopg.connect(host="127.0.0.1", dbname="fastapi", user="postgres", password="admin_001", row_factory=dict_row)

    cursor = conn.cursor()
    print("Database connection was succesfull!")
    
    break
  except Exception as error:
    print("Connecting to database failed!")
    print(f"Error was: {error}")
    time.sleep(2)


my_posts = [
  {
    "title": "Best programming languges to learn in 2025",
    "content": "I don't know :D",
    "id": 1
  },
  {
    "title": "Favourite foods",
    "content": "I like pizza",
    "id": 2,
  }
]


def find_post(id):
  for post in my_posts:
    if post["id"] == id:
      return post
    

def find_index_post(id):
  for index, post in enumerate(my_posts):
    if post["id"] == id:
      return index


@app.get("/")
def root():
  return {"message": "Hellooooo!"}


@app.get("/posts")
def get_posts():
  cursor.execute("""SELECT * FROM posts""")
  posts = cursor.fetchall()
  return {"posts": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED) 
def create_post(post: Post):
  cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
  new_post = cursor.fetchone()
  conn.commit()
  return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
  cursor.execute(f"SELECT * FROM posts WHERE id={id}")
  post = cursor.fetchone()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found!")
  
  return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
  cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
  deleted_post = cursor.fetchone()
  conn.commit()
  if deleted_post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist!")
  
  return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
  cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""", (post.title, post.content, post.published, str(id)))
  updated_post = cursor.fetchone()
  conn.commit()
  if updated_post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist!")

  return {"data": updated_post}
