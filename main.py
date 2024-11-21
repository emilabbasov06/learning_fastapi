from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
  return {"message": "Hellooooo!"}


@app.get("/")
def get_posts():
  return {"data" : "This is your posts"}