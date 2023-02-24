from fastapi import FastAPI

app = FastAPI()

@app.post("/auth/login/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id + 1 , "q": q}