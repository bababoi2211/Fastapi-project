

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
# SQLALCHEMY_DATABASE_URL = 'postgressql://postgres:dani1383@localhost/fastapi'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
print("Data Base Connection Was Succesful")

def get_db():
    db = Session_local()

    try:
        yield db
    finally:
        db.close()
