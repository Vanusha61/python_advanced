import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

db_url = os.getenv("DB_URL")
if db_url is None:
    raise ValueError("DB_URL environment variable not set")
engine = create_engine(db_url, echo=False)
session = sessionmaker(
    bind=engine, autocommit=False, autoflush=True, expire_on_commit=False
)

base = declarative_base()
