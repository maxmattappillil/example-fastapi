from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# Responsible for establishing the connection to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# To talk to the database, you have to make a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All the models that we'll define to make Tables in Postgres will extend from the Baseclass --> sqlalchemy.ext.declarative.declarative_base
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()