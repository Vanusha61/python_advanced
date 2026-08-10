from sqlalchemy import (
    create_engine,
    Column,
    Text,
    Integer,
    Date, Float, Boolean, DateTime)
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime

engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)


class Base(declarative_base()):
    pass


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, nullable=False)


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    @classmethod
    def get_all_students_scholarship(cls) -> list[Student]:
        with Session() as session:
            students = session.query(cls).filter(cls.scholarship).all()
            return students

    @classmethod
    def get_all_students_average_score(cls, ball: float) -> list[Student]:
        with Session() as session:
            students = session.query(cls).filter(cls.average_score > ball).all()
            return students



class ReceivingBooks(Base):
    __tablename__ = 'receiving_books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime)

    @hybrid_property
    def count_date_with_book(self):
        if self.date_of_return is None:
            delta = datetime.now() - self.date_of_issue
        else:
            delta = self.date_of_return - self.date_of_issue
        return delta.days