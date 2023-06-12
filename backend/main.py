from fastapi import FastAPI
from core import settings

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}