from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DB_URL = "postgresql+psycopg2://postgres:password@db:5432/skillbox_db"
engine = create_engine(DB_URL, echo=True)
session = sessionmaker(bind=engine, autocommit=False)
