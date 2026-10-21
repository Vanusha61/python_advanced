import logging.config

from app.config import session
from app.extensions import dict_config_crud
from app.models.database import Media, User

logging.config.dictConfig(dict_config_crud)
logger = logging.getLogger("crud_logger")


class UserNotFound(Exception):
    pass


def crud_create_media(api_key: str, file_path: str) -> Media | None:
    try:
        with session() as db_session:
            logger.debug("Start crud_create_media")
            user = db_session.query(User).filter(User.api_key == api_key).first()
            logger.debug("search user in db")
            if not user:
                logger.warning("User not found in db")
                raise UserNotFound("User not found")
            media = Media(
                file_path=file_path,
            )
            db_session.add(media)
            logger.debug("add media to db")
            db_session.commit()
            logger.debug("commit media to db")
            db_session.refresh(media)
            return media
    except Exception as err:
        logger.error(err)
        db_session.rollback()
        return None
