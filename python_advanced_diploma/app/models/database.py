from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.config import base


class User(base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    api_key = Column(String, nullable=False, unique=True)
    tweets = relationship(
        "Tweet", back_populates="user", lazy="selectin", cascade="all, delete-orphan"
    )
    following = relationship(
        "Follow",
        foreign_keys="Follow.follower_id",
        back_populates="follower",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    followers = relationship(
        "Follow",
        foreign_keys="Follow.followed_id",
        back_populates="followed",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, api_key: {self.api_key}"


class Tweet(base):
    __tablename__ = "tweet"
    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    content = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    user = relationship("User", back_populates="tweets", lazy="selectin")
    likes = relationship(
        "Like", back_populates="tweet", lazy="selectin", cascade="all, delete-orphan"
    )
    media = relationship("Media", lazy="joined", cascade="all, delete-orphan")

    def __repr__(self):
        return f"id: {self.id}, author_id: {self.author_id}, content: {self.content}, created_at: {self.created_at}"


class Like(base):
    __tablename__ = "like"
    __table_args__ = (UniqueConstraint("user_id", "tweet_id", name="unique_tweet"),)
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    tweet_id = Column(
        Integer, ForeignKey("tweet.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", lazy="joined")
    tweet = relationship("Tweet", back_populates="likes", lazy="selectin")

    def __repr__(self):
        return f"id: {self.id}, user_id: {self.user_id}, tweet_id: {self.tweet_id}"


class Follow(base):
    __tablename__ = "follow"
    __table_args__ = (
        UniqueConstraint("follower_id", "followed_id", name="unique_follow"),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    follower_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    followed_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    follower = relationship(
        "User", foreign_keys=[follower_id], back_populates="following", lazy="selectin"
    )
    followed = relationship(
        "User", foreign_keys=[followed_id], back_populates="followers", lazy="selectin"
    )

    def __repr__(self):
        return f"id: {self.id}, follower_id: {self.follower_id}, followed_id: {self.followed_id}"


class Media(base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tweet_id = Column(
        Integer, ForeignKey("tweet.id", ondelete="CASCADE"), nullable=True
    )
    file_path = Column(String, nullable=False)

    def __repr__(self):
        return f"id: {self.id}, tweet_id: {self.tweet_id}"
