import sqlite3
from typing import Any

from module_05_processes_and_threads.homework.hw5_add.self_printing import result


def add_room(floor: int, beds: int, guest_num: int, price: int) -> None:
    with sqlite3.connect("database.db") as coon:
        cursor = coon.cursor()
        cursor.execute(
            """
            INSERT INTO room (floor, beds, guest_num, price)
            VALUES (?, ?, ?, ?)
            """, (floor, beds, guest_num, price)
        )
        coon.commit()
        return cursor.lastrowid


def all_rooms(chek_in: str = None, chek_out: str = None) -> list[Any]:
    with sqlite3.connect("database.db") as coon:
        cursor = coon.cursor()
        if chek_in and chek_out:
            cursor.execute(
                """
                SELECT *
                FROM room r
                WHERE r.id NOT IN (
                    SELECT b.room_id
                    FROM booking b
                    WHERE b.check_in < ? AND b.check_out > ?
                )
                """, (chek_out, chek_in)
            )
            rooms = cursor.fetchall()
            return rooms

        cursor.execute(
            """
            SELECT *
            FROM room
            """
        )
        rooms = cursor.fetchall()
        return rooms

def add_booking(room_id, check_in, check_out, first_name, last_name) -> str | None:
    with sqlite3.connect("database.db") as coon:
        try:
            coon.execute("PRAGMA foreign_keys = ON")
            cursor = coon.cursor()
            cursor.execute(
                """
                SELECT count(*) FROM booking b
                WHERE  b.room_id = ? and b.check_in < ? and b.check_out > ?
                """, (room_id, check_out, check_in)
            )
            count = cursor.fetchone()[0]
            if count > 0:
                return "На эту дату комната уже забронирована"
            cursor.execute(
                """
                INSERT INTO booking (room_id, check_in, check_out, first_name, last_name) VALUES (?, ?, ?, ?, ?)
                """, (room_id, check_in, check_out, first_name, last_name)
            )
            coon.commit()
        except sqlite3.IntegrityError:
            return "Добавьте сначала room"


