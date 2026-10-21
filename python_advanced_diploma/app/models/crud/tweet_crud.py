import logging.config

from app.config import session
from app.extensions import dict_config_crud
from app.models.database import Like, Media, Tweet, User

logging.config.dictConfig(dict_config_crud)
logger = logging.getLogger("crud_logger")


class UserNotFoundErrorTweet(Exception):
    pass


class TweetNotFoundError(Exception):
    pass


class PermissionError(Exception):
    pass


class MediaAlreadyAttachedError(Exception):
    pass


class MediaNotFoundError(Exception):
    pass


class AuthorTweetError(Exception):
    pass


class LikeTweetError(Exception):
    pass


def crud_create_tweet(
    api_key: str, content: str, media_ids: list[int] | None = None
) -> Tweet | None:
    try:
        with session() as conn:
            logger.debug("start create tweet")
            user = conn.query(User).filter(User.api_key == api_key).first()
            logger.debug("search user in api_key from db")
            if user is None:
                logger.warning("No found user in api_key")
                raise UserNotFoundErrorTweet("No found user in api_key")
            tweet = Tweet(
                content=content,
                author_id=user.id,
            )
            conn.add(tweet)
            logger.debug("add tweet into db")
            conn.flush()
            if media_ids:
                logger.debug("add media id in db")
                for med in media_ids:
                    media = conn.query(Media).filter(Media.id == med).first()
                    if not media:
                        raise MediaNotFoundError("Media not found")
                    if media.tweet_id is not None:
                        raise MediaAlreadyAttachedError("Media already attached")
                    media.tweet_id = tweet.id
            conn.commit()
            logger.debug("commit tweet into db")
            conn.refresh(tweet)
            logger.debug("close db")
            return tweet
    except UserNotFoundErrorTweet:
        raise
    except MediaAlreadyAttachedError:
        raise
    except MediaNotFoundError:
        raise
    except Exception as ex:
        logger.error(ex)
        conn.rollback()
        return None


def crud_delete_tweet_id(api_key: str, tweet_id: int) -> bool | None:
    try:
        with session() as conn:
            logger.debug("start delete tweet")
            user = conn.query(User).filter(User.api_key == api_key).first()
            logger.debug("search user in api_key from db")
            if user is None:
                logger.warning("No found user in api_key")
                raise UserNotFoundErrorTweet("No found user in api_key")
            tweet = conn.query(Tweet).filter(Tweet.id == tweet_id).first()
            logger.debug("search tweet in db")
            if tweet is None:
                logger.warning("No found tweet in db")
                raise TweetNotFoundError("No found tweet in db")
            if tweet.author_id != user.id:
                logger.warning("Author id not equal to author_id")
                raise AuthorTweetError("Author id not equal to author_id")
            conn.delete(tweet)
            logger.debug("delete tweet into db")
            conn.commit()
            logger.debug("close db")
            return True
    except UserNotFoundErrorTweet:
        raise
    except TweetNotFoundError:
        raise
    except AuthorTweetError:
        raise
    except Exception as ex:
        logger.error(ex)
        conn.rollback()
        return None


def crud_created_like_tweet(api_key: str, tweet_id: int) -> bool | None:
    try:
        with session() as conn:
            logger.debug("start create tweet")
            user = conn.query(User).filter(User.api_key == api_key).first()
            logger.debug("search user in api_key from db")
            if user is None:
                logger.warning("No found user in api_key")
                raise UserNotFoundErrorTweet("No found user in api_key")
            tweet = conn.query(Tweet).filter(Tweet.id == tweet_id).first()
            logger.debug("search tweet in db")
            if tweet is None:
                logger.warning("No found tweet in db")
                raise TweetNotFoundError("No found tweet in db")
            like = (
                conn.query(Like)
                .filter(Like.tweet_id == tweet.id, Like.user_id == user.id)
                .first()
            )
            logger.debug("search like in db")
            if like:
                logger.warning("Вы уже ставили лайк пользователю по этим постом")
                raise LikeTweetError("Вы уже ставили лайк пользователю по этим постом")
            like = Like(
                user_id=user.id,
                tweet_id=tweet.id,
            )
            conn.add(like)
            logger.debug("add like into db")
            conn.commit()
            logger.debug("commit like into db")
            conn.refresh(like)
            logger.debug("close db")
            return True
    except UserNotFoundErrorTweet:
        raise
    except TweetNotFoundError:
        raise
    except LikeTweetError:
        raise
    except Exception as ex:
        logger.error(ex)
        conn.rollback()
        return None


def crud_delete_like_tweet(api_key: str, tweet_id: int) -> bool | None:
    try:
        with session() as conn:
            logger.debug("start delete tweet")
            user = conn.query(User).filter(User.api_key == api_key).first()
            logger.debug("search user in api_key from db")
            if user is None:
                logger.warning("No found user in api_key")
                raise UserNotFoundErrorTweet("No found user in api_key")
            tweet = conn.query(Tweet).filter(Tweet.id == tweet_id).first()
            logger.debug("search tweet in db")
            if tweet is None:
                logger.warning("No found tweet in db")
                raise TweetNotFoundError("No found tweet in db")
            like = (
                conn.query(Like)
                .filter(
                    Like.tweet_id == tweet.id,
                    Like.user_id == user.id,
                )
                .first()
            )
            logger.debug("search like in db")
            if like is None:
                logger.warning("No found like in db")
                raise LikeTweetError("No found like in db")
            conn.delete(like)
            logger.debug("delete like into db")
            conn.commit()
            logger.debug("close db")
            return True
    except UserNotFoundErrorTweet:
        raise
    except TweetNotFoundError:
        raise
    except LikeTweetError:
        raise
    except Exception as ex:
        logger.error(ex)
        conn.rollback()
        return None
