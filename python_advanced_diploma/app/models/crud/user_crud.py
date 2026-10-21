import logging.config
from typing import List

from sqlalchemy import desc, func, or_

from app.config import session
from app.extensions import dict_config_crud
from app.models.database import Follow, Like, Tweet, User

logging.config.dictConfig(dict_config_crud)
logger = logging.getLogger("crud_logger")


class UserNotFoundError(Exception):
    pass


class FollowNotFoundError(Exception):
    pass


def crud_user_follower(api_key: str, user_id: int) -> bool | None:
    try:
        with session() as db_session:
            logger.debug("starting follower crud operation")
            user = db_session.query(User).filter(User.api_key == api_key).first()
            if user is None:
                logger.warning("not found user")
                raise UserNotFoundError("not found user")
            user_api_key = db_session.query(User).filter(User.id == user_id).first()
            if user_api_key is None:
                logger.warning("not found user")
                raise UserNotFoundError("not found user")
            follower = (
                db_session.query(Follow)
                .filter(Follow.follower_id == user.id, Follow.followed_id == user_id)
                .first()
            )
            if follower:
                logger.warning("you follow for user")
                raise FollowNotFoundError("you follow for user")

            follow_user = Follow(follower_id=user.id, followed_id=user_id)
            db_session.add(follow_user)
            logger.debug("add follow user in db")
            db_session.commit()
            logger.debug("commit follow user in db")
            db_session.refresh(follow_user)
            logger.debug("close in db")
            return True
    except UserNotFoundError:
        raise
    except FollowNotFoundError:
        raise
    except Exception as e:
        logger.error(e)
        db_session.rollback()
        return None


def crud_delete_user_follow(api_key: str, user_id: int) -> bool | None:
    try:
        with session() as db_session:
            logger.debug("starting follower crud operation")
            user = db_session.query(User).filter(User.api_key == api_key).first()
            if user is None:
                logger.warning("not found user")
                raise UserNotFoundError("not found user")
            user_api_key = db_session.query(User).filter(User.id == user_id).first()
            if user_api_key is None:
                logger.warning("not found user")
                raise UserNotFoundError("not found user")
            follower = (
                db_session.query(Follow)
                .filter(Follow.follower_id == user.id, Follow.followed_id == user_id)
                .first()
            )
            if not follower:
                logger.warning("not  fallow for user")
                raise FollowNotFoundError("not found fallow for user")
            db_session.delete(follower)
            logger.debug("delete follow user in db")
            db_session.commit()
            logger.debug("commit follow user in db")
            return True
    except UserNotFoundError:
        raise
    except FollowNotFoundError:
        raise
    except Exception as e:
        logger.error(e)
        db_session.rollback()
        return None


def crud_user_tweets(api_key: str) -> List[Tweet]:
    try:
        with session() as db_session:
            logger.debug("starting tweets_list crud operation")
            user = db_session.query(User).filter(User.api_key == api_key).first()
            logger.debug("search user in db")
            if user is None:
                raise UserNotFoundError("not found user")
            tweets = (
                db_session.query(
                    Tweet,
                )
                .outerjoin(Follow, Follow.followed_id == Tweet.author_id)
                .filter(
                    or_(
                        Follow.follower_id == user.id,
                        Tweet.author_id == user.id,
                    )
                )
                .outerjoin(Like, Like.tweet_id == Tweet.id)
                .group_by(Tweet.id)
                .order_by(desc(func.count(Like.id)))
                .all()
            )
            logger.debug("finish tweets_list crud operation")
            return tweets
    except UserNotFoundError:
        logger.warning("not found user")
        raise
    except Exception as e:
        logger.error(e)
        raise


def crud_user_me(api_key: str) -> User | None:
    try:
        with session() as db_session:
            logger.debug("starting me crud operation")
            user = db_session.query(User).filter(User.api_key == api_key).first()
            if user is None:
                logger.warning("not found user")
                raise UserNotFoundError("not found user")
            return user
    except UserNotFoundError:
        raise
    except Exception as e:
        logger.error(e)
        return None


def crud_user_id(user_id) -> User | None:
    try:
        with session() as db_session:
            logger.debug("starting me crud operation")
            user = db_session.query(User).filter(User.id == user_id).first()
            if user is None:
                logger.warning("not found user")
                raise UserNotFoundError("not found user")
            return user
    except UserNotFoundError:
        raise
    except Exception as e:
        logger.error(e)
        return None


if __name__ == "__main__":
    crud_user_tweets(api_key="key_1_abc123")
