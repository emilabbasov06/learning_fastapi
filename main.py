from fastapi import FastAPI, Response, status, HTTPException
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
  return {"posts": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED) 
def create_post(post: Post):
  post_dict = post.dict()
  post_dict["id"] = randrange(0, 99999999)
  my_posts.append(post_dict)
  return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int):
  post = find_post(id)
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found!")
  
  return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
  index = find_index_post(id)
  if index == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist!")
  my_posts.pop(index)
  
  return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
  index = find_index_post(id)
  if index == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist!")
  
  post_dict = post.dict()
  post_dict["id"] = id
  my_posts[index] = post_dict  
  return {"data": post_dict}
