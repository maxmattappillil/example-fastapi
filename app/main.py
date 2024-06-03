from fastapi import FastAPI, status
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# Need this to create tables in the database that's based on the models we constructed
# --> metadata: this attribute holds a collcetion of table objects and their assocaited schema constructs
# --> create_all(): this iterates over all the table objects and attemps to make them in the database if they're not already present
# --> bind=engine: This specifies the database connection to use for creating the tables

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World"}