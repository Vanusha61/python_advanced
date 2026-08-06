import sqlite3
from typing import Any, Optional, List

DATA: List[dict] = [
    {'id': 0, 'title': 'A Byte of Python', 'author': 'Swaroop C. H.'},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 'Herman Melville'},
    {'id': 3, 'title': 'War and Peace', 'author': 'Leo Tolstoy'},
]


class Book:

    def __init__(self, id: int, title: str, author: str, views_count: int) -> None:
        self.id: int = id
        self.title: str = title
        self.author: str = author
        self.views_count = views_count

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


def init_db(initial_records: List[dict]) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='table_books'; 
            """
        )
        exists: Optional[tuple[str,]] = cursor.fetchone()
        # now in `exist` we have tuple with table name if table really exists in DB
        if not exists:
            cursor.executescript(
                """
                CREATE TABLE `table_books` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT, 
                    author TEXT,
                    views_count INTEGER DEFAULT 0
                )
                """
            )
            cursor.executemany(
                """
                INSERT INTO `table_books`
                (title, author) VALUES (?, ?)
                """,
                [
                    (item['title'], item['author'])
                    for item in initial_records
                ]
            )


def get_all_books() -> List[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * from `table_books`
            """
        )
        return [Book(*row) for row in cursor.fetchall()]

def add_book(title: str, author: str) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO `table_books` (title, author) values (?, ?)
            """, (title, author)
        )
        conn.commit()

def author_all_books(author_name: str) -> List[str]:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * from `table_books`
            WHERE author = ?
            """, (author_name, )
        )
        res = cursor.fetchall()
        return [l[1] for l in res]


def add_row() -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            ALTER TABLE `table_books` 
            ADD COLUMN views_count INTEGER DEFAULT 0
            """
        )

def add_views_count(book_id: int):
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE `table_books` 
            SET views_count = views_count + 1
            WHERE id = ?
            """, (book_id, )
        )
        cursor.execute(
            """
            SELECT * FROM `table_books` WHERE id = ?
            """, (book_id, )
        )
        result = cursor.fetchone()
        if result is None:
            return None
        res = "id: {}, title: {}, author: {}, views_count: {}"
        return res.format(result[0], result[1], result[2], result[3])


