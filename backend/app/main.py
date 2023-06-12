from fastapi import FastAPI
from .core import settings

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "Worldo"}


@app.get("/health-check")
def read_root():
    return {
        "db": settings.mysql_database
    }
