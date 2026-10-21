from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import app.config as _config
import app.models.crud.media_crud as media_crud
import app.models.crud.tweet_crud as tweet_crud
import app.models.crud.user_crud as user_crud
import pytest
from app.models.database import Follow, Tweet, User, base
from run import app as _app


@pytest.fixture
def session():
    engine = create_engine("sqlite://", echo=False)
    base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    yield session
    base.metadata.drop_all(engine)


@pytest.fixture
def app(session: Session, monkeypatch):
    monkeypatch.setattr(_config, "session", session)
    monkeypatch.setattr(media_crud, "session", session)
    monkeypatch.setattr(tweet_crud, "session", session)
    monkeypatch.setattr(user_crud, "session", session)
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    with session() as db_session:
        user1 = User(
            name="user1",
            api_key="api_key1",
        )
        user2 = User(
            name="user2",
            api_key="api_key2",
        )
        user3 = User(
            name="user3",
            api_key="api_key3",
        )
        db_session.add_all([user1, user2, user3])
        db_session.commit()
        tweet1 = Tweet(
            author_id=user1.id,
            content="This is the content user1",
        )
        tweet2 = Tweet(
            author_id=user2.id,
            content="This is the content user2",
        )
        db_session.add_all([tweet1, tweet2])
        follow_user1 = Follow(
            follower_id=user1.id,
            followed_id=user2.id,
        )
        db_session.add(follow_user1)
        db_session.commit()
    yield _app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(session: Session):
    with session() as db_session:
        yield db_session
