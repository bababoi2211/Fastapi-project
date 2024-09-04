
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from database import engine
import models
from routers import product, user, auth, vote

# connection


models.Base.metadata.create_all(bind=engine)


app = FastAPI()
origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(product.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
