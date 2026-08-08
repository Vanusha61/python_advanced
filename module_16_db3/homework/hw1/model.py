import sqlite3

def created_all():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('''
        PRAGMA foreign_keys = ON
        ''')
        cur.execute('DROP TABLE IF EXISTS movie_cast;')
        cur.execute('DROP TABLE IF EXISTS oscar_awarded;')
        cur.execute('DROP TABLE IF EXISTS movie_direction;')

        cur.execute('DROP TABLE IF EXISTS actors;')
        cur.execute('DROP TABLE IF EXISTS movie;')
        cur.execute('DROP TABLE IF EXISTS director;')

        cur.execute('''
        CREATE TABLE actors (
            act_id INTEGER PRIMARY KEY AUTOINCREMENT,
            act_first_name TEXT,
            act_last_name TEXT,
            act_gender TEXT
        )
        ''')
        cur.execute('''
        CREATE TABLE movie (
            mov_id INTEGER PRIMARY KEY AUTOINCREMENT,
            mov_title TEXT
        )
        ''')

        cur.execute('''
        CREATE TABLE director (
            dir_id INTEGER PRIMARY KEY AUTOINCREMENT,
            dir_first_name TEXT,
            dir_last_name TEXT
        )
        ''')

        cur.execute('''
        CREATE TABLE movie_cast (
            act_id INTEGER references actors(act_id) on delete cascade,
            mov_id INTEGER references movie(mov_id) on delete cascade,
            role Text
        )
        ''')

        cur.execute('''
        CREATE TABLE oscar_awarded (
            award_id INTEGER PRIMARY KEY AUTOINCREMENT,
            mov_id INTEGER references movie(mov_id) on delete cascade
        )
        ''')

        cur.execute('''
        CREATE TABLE movie_direction (
            dir_id INTEGER references director(dir_id) on delete cascade,
            mov_id INTEGER references movie(mov_id) on delete cascade
        )
        ''')