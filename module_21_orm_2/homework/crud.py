from typing import List

from config import Session, Book, ReceivingBooks, Student
from module_21_orm_2.homework.config import Book

from datetime import datetime
from sqlalchemy import func

def get_top_10_student() -> List[dict] | None:
    with Session() as session:
        current_year = datetime.now().year
        result = session.query(
            ReceivingBooks.student_id,
            func.count().label('books_count')
        ).filter(
            func.extract('year', ReceivingBooks.date_of_issue) == current_year
        ).group_by(
            ReceivingBooks.student_id
        ).order_by('books_count desc').limit(10).subquery()
        student = session.query(Student).filter(Student.id.in_(result.c.student_id)).all()
        return student or None

def get_month_books():
    with Session() as session:
        current_month = datetime.now().month
        current_year = datetime.now().year
        result = session.query(
            ReceivingBooks.student_id,
            func.count().label('books_count')
        ).filter(
            func.extract('year', ReceivingBooks.date_of_issue) == current_year,
            func.extract('month', ReceivingBooks.date_of_issue) == current_month
        ).group_by(ReceivingBooks.student_id).subquery()
        avg_resul = session.query(func.avg(result.c.books_count)).scalar()
        return avg_resul or 0.0

def get_student_balls_avg():
    with Session() as session:
        result = session.query(Student.id).filter(Student.average_score > 4).subquery()
        book = session.query(
            ReceivingBooks.book_id,
            func.count().label('books_count')
            ).filter(
            ReceivingBooks.student_id.in_(result)
        ).group_by(ReceivingBooks.book_id).order_by('books_count desc').limit(1).scalar()
        return session.query(Book).filter(Book.id == book).scalar()



def get_count_books(author_id: int) -> int:
    with Session() as session:
        books_receiving = session.query(ReceivingBooks).filter(ReceivingBooks.date_of_return.is_(None)).all()
        books_id = set(b_id.book_id for b_id in books_receiving)
        books_all = session.query(Book).filter(Book.author_id == author_id,Book.id.not_in(books_id)).count()
        return books_all


def get_books_student_not_author(students_id:int) -> List[Book] | None:
    with Session() as session:
        books_receiving = session.query(ReceivingBooks).filter(ReceivingBooks.student_id == students_id).all()
        if not books_receiving:
            return None
        read_book_ids = {b.book_id for b in books_receiving}
        author_ids = {b.book.author_id for b in books_receiving}
        books_authors = session.query(Book).filter(Book.id.not_in(read_book_ids), Book.author_id.in_(author_ids)).all()
        return books_authors


def book_to_dict(book: Book) -> dict:
    return {
        'id': book.id,
        'name': book.name,
        'count': book.count,
        'release_date': book.release_date.isoformat() if book.release_date else None,
        'author_id': book.author_id
    }

def books_to_list(books: List[Book]) -> List[dict]:
    return [book_to_dict(b) for b in books]

def student_with_books_to_dict(student: Student) -> dict:
    return {
        'id': student.id,
        'name': student.name,
        'surname': student.surname,
        'phone': student.phone,
        'email': student.email,
        'average_score': student.average_score,
        'scholarship': student.scholarship,
        'books': [book_to_dict(b) for b in student.books]
    }
