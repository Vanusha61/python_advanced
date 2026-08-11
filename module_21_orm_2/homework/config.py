from sqlalchemy import (
    create_engine,
    Column,
    Text,
    Integer,
    Date, Float, Boolean, DateTime, func, case)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
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
    author_id = Column(Integer, nullable=False, foreign_key='author.id', ondelete='CASCADE')
    author = relationship("Author", back_populates="books", lazy="selectin")
    receivings = relationship("ReceivingBooks", back_populates="book", lazy="selectin")
    students = association_proxy("receivings", "student")

class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    books = relationship("Book", back_populates="author", lazy="selectin")


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)
    receivings = relationship("ReceivingBooks", back_populates="student", lazy="selectin")
    books = association_proxy("receivings", "book")

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
    book_id = Column(Integer, nullable=False, foreign_key='book.id')
    book = relationship("Book", lazy="joined" ,uselist=False, back_populates="receivings")
    student_id = Column(Integer, nullable=False, foreign_key='student.id')
    student = relationship("Student", uselist=False, lazy="joined", back_populates="receivings")
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime)

    @hybrid_property
    def count_date_with_book(self):
        # Python-вычисление для экземпляров
        if self.date_of_return is None:
            delta = datetime.now() - self.date_of_issue
        else:
            delta = self.date_of_return - self.date_of_issue
        return delta.days

    @count_date_with_book.expression
    def count_date_with_book(cls):
        # SQL-выражение для использования в запросах
        end_date = case(
            (cls.date_of_return != None, cls.date_of_return),
            else_=func.now()
        )
        return func.julianday(end_date) - func.julianday(cls.date_of_issue)
