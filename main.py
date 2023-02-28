from fastapi import Body, FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hellow world!"}


@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}

@app.post("/posts")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"new post": f"title: {payload['title']}, id: {payload['id']}"}
