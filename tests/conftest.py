from fastapi.testclient import TestClient
import pytest
import sqlalchemy
import sqlalchemy.dialects
from app.main import app
from app import schemas

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app import models
from app.database import get_db, Base

from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

#Use this for local development
# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

# Responsible for establishing the connection to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# To talk to the database, you have to make a session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        yield session
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "sanjeev@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "sanjeev123@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "Title 1",
        "content": "1st content",
        "owner_id": test_user['id']
    }, {
        "title": "Title 2",
        "content": "2nd content",
        "owner_id": test_user['id']
    },{
        "title": "Title 3",
        "content": "3rd content",
        "owner_id": test_user['id']
    },{
        "title": "Title 4",
        "content": "4th content",
        "owner_id": test_user2['id']
    }]

    posts = [models.Post(**post) for post in posts_data]

    session.add_all(posts)
    session.commit()
    
    posts = session.query(models.Post).order_by(models.Post.title).all()
    return posts