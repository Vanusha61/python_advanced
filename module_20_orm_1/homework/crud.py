from datetime import datetime

from sqlalchemy import func

from typing import List

from config import Session, Student, Book, ReceivingBooks


def crud_get_all_books() -> List[Book]:
    with Session() as session:
        books = session.query(Book).all()
        return books

def crud_get_all_debtors_students() -> List[Student]:
    with Session() as session:
        students = session.query(Student).join(ReceivingBooks, Student.id == ReceivingBooks.student_id).filter(
            ReceivingBooks.date_of_return.is_(None), (ReceivingBooks.count_date_with_book > 14)).all()
        return students

def crud_post_to_give_book(student_id: int, book_id: int):
    try:
        with Session() as session:
            result = session.query(ReceivingBooks).filter(
                ReceivingBooks.student_id == student_id, ReceivingBooks.book_id == book_id, ReceivingBooks.date_of_return.is_(None)
            ).one_or_none()
            if result:
                return None
            new_receiving_book = ReceivingBooks(
                student_id=student_id,
                book_id=book_id,
                date_of_issue=datetime.now()
            )
            session.add(new_receiving_book)
            session.commit()
            session.refresh(new_receiving_book)
            return new_receiving_book
    except Exception as ex:
        session.rollback()
        print(ex)

def crud_post_back_book(student_id: int, book_id: int):
    try:
        with Session() as session:
            result = session.query(ReceivingBooks).filter(
                ReceivingBooks.student_id == student_id, ReceivingBooks.book_id == book_id, ReceivingBooks.date_of_return.is_(None)
            ).one_or_none()
            if result:
                result.date_of_return = datetime.now()
                session.add(result)
                session.commit()
                session.refresh(result)
                return result
            return None
    except Exception as ex:
        session.rollback()
        print(ex)


def book_to_dict(book: Book) -> dict:
    return {
        'id': book.id,
        'name': book.name,
        'count': book.count,
        'release_date': book.release_date.isoformat() if book.release_date else None,
        'author_id': book.author_id
    }

def student_to_dict(student: Student) -> dict:
    return {
        'id': student.id,
        'name': student.name,
        'surname': student.surname,
        'phone': student.phone,
        'email': student.email,
        'average_score': student.average_score,
        'scholarship': student.scholarship
    }

def receiving_to_dict(record: ReceivingBooks) -> dict:
    return {
        'id': record.id,
        'book_id': record.book_id,
        'student_id': record.student_id,
        'date_of_issue': record.date_of_issue.isoformat() if record.date_of_issue else None,
        'date_of_return': record.date_of_return.isoformat() if record.date_of_return else None,
        'count_days': record.count_date_with_book
    }

def crud_search_books_by_name(book_name: str) -> List[Book]:
    with Session() as session:
        book = session.query(Book).filter(Book.name.like(f"%{book_name}%")).all()
        if book:
            return book
        return None

