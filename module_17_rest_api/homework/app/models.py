import sqlite3
from dataclasses import dataclass
from typing import Optional, Union, List, Dict

DATA = [
    {'id': 0, 'title': 'A Byte of Python', 'author': 'Swaroop C. H.'},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 'Herman Melville'},
    {'id': 3, 'title': 'War and Peace', 'author': 'Leo Tolstoy'},
]

DATABASE_NAME = 'table_books.db'
BOOKS_TABLE_NAME = 'books'
AUTHORS_TABLE_NAME = 'authors'


@dataclass
class Book:
    title: str
    author_id: int
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


@dataclass
class Author:
    first_name: str
    last_name: str
    middle_name: str | None = None
    id: int | None = None



def init_db(initial_records: List[Dict]) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Создаём таблицу авторов, если её нет
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {AUTHORS_TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                middle_name TEXT
            );
        """)

        # Создаём таблицу книг, если её нет
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {BOOKS_TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author_id INTEGER REFERENCES {AUTHORS_TABLE_NAME}(id) ON DELETE CASCADE
            );
        """)

        # Извлекаем уникальные имена авторов из initial_records
        unique_authors = {record['author'] for record in initial_records}

        # Сопоставляем полное имя -> ID в БД
        author_name_to_id = {}

        for full_name in unique_authors:
            # Простейший парсинг: разбиваем по пробелам
            parts = full_name.split()
            if len(parts) == 3:
                first, middle, last = parts
            elif len(parts) == 2:
                first, last = parts
                middle = None
            else:
                # Если имя нестандартное – сохраняем всё в first_name
                first, last = full_name, ""
                middle = None

            cursor.execute(
                f"INSERT INTO {AUTHORS_TABLE_NAME} (first_name, last_name, middle_name) VALUES (?, ?, ?)",
                (first, last, middle)
            )
            author_id = cursor.lastrowid
            author_name_to_id[full_name] = author_id

        # Вставляем книги, используя полученные ID авторов
        books_data = [
            (record['title'], author_name_to_id[record['author']])
            for record in initial_records
        ]
        cursor.executemany(
            f"INSERT INTO {BOOKS_TABLE_NAME} (title, author_id) VALUES (?, ?)",
            books_data
        )
        conn.commit()


def _get_book_obj_from_row(row: tuple) -> Book:
    return Book(id=row[0], title=row[1], author_id=row[2])



def get_all_books() -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{BOOKS_TABLE_NAME}`')
        all_books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in all_books]


def add_book(book: Book) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{BOOKS_TABLE_NAME}` 
            (title, author_id) VALUES (?, ?)
            """,
            (book.title, book.author_id)
        )
        book.id = cursor.lastrowid
        return book


def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE id = ?
            """,
            (book_id,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def update_book_by_id(book: Book) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE {BOOKS_TABLE_NAME}
            SET title = ?, author_id = ?
            WHERE id = ?
            """,
            (book.title, book.author_id, book.id)
        )
        conn.commit()


def delete_book_by_id(book_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {BOOKS_TABLE_NAME}
            WHERE id = ?
            """,
            (book_id,)
        )
        conn.commit()


def get_book_by_title(book_title: str) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE title = ?
            """,
            (book_title,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)

def _get_author_obj_from_row(row: tuple) -> Author:
    return Author(id=row[0], first_name=row[1], last_name=row[2], middle_name=row[3])

def get_all_authors():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{AUTHORS_TABLE_NAME}` 
            """
        )
        authors = cursor.fetchall()
        return [_get_author_obj_from_row(aut) for aut in authors]

def add_author(author: Author) -> Author:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO {AUTHORS_TABLE_NAME} (first_name, last_name, middle_name)
            VALUES (?, ?, ?)
            """,
            (author.first_name, author.last_name, author.middle_name)
        )
        author.id = cursor.lastrowid
        return author

def get_author_all_book_by_id(author_id: int) -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE author_id = ?
            """, (author_id,)
        )
        books = cursor.fetchall()
        if books:
            return [_get_book_obj_from_row(book) for book in books]

def delete_author_by_id(author_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {AUTHORS_TABLE_NAME} WHERE id = ?
            """, (author_id,)
        )
        conn.commit()