from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


class Post(BaseModel):
  title: str
  content: str
  published: bool = True
  rating: Optional[int] = None


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

@app.get("/")
def root():
  return {"message": "Hellooooo!"}


@app.get("/posts")
def get_posts():
  return {"posts": my_posts}


@app.post("/posts") 
def create_post(post: Post):
  post_dict = post.dict()
  post_dict["id"] = randrange(0, 99999999)
  
  my_posts.append(post_dict)
  return {"data": post_dict}