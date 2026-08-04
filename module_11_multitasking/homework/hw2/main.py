import sqlite3
import threading
import requests
import time

from queue import Queue

queue_list = Queue()


def star_people(id: int, queue: Queue):
    api_star = "https://www.swapi.tech/api/people/{}".format(id)
    response = requests.get(api_star, timeout=10)
    if response.status_code == 200:
        data = response.json()['result']['properties']
        name = data.get('name', "No name")
        gender = data.get('gender', "No gender")
        old = data.get('birth_year', "no birth_year")
        queue.put((name, gender, old))

def star_people_sinc(id: int, queue: Queue):
    api_star = "https://www.swapi.tech/api/people/{}".format(id)
    response = requests.get(api_star, timeout=10)
    if response.status_code == 200:
        data = response.json()['result']['properties']
        name = data.get('name', "No name")
        gender = data.get('gender', "No gender")
        old = data.get('birth_year', "no birth_year")
        queue.put((name, gender, old))



if __name__ == '__main__':
    start = time.time()
    threads = []
    for i in range(1, 21):
        thread = threading.Thread(target=star_people, args=(i, queue_list))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    characters = []
    while not queue_list.empty():
        characters.append(queue_list.get())

    conn = sqlite3.connect('star_people.db')
    cursor = conn.cursor()
    cursor.executemany(
        'INSERT INTO star_people (name, gender, age) VALUES (?, ?, ?)',
        characters
    )
    conn.commit()
    conn.close()
    print("--- %s seconds ---" % (time.time() - start))

    start_sinc = time.time()
    for i in range(1, 21):
        star_people_sinc(i, queue_list)
    characters = []
    while not queue_list.empty():
        characters.append(queue_list.get())

    conn = sqlite3.connect('star_people.db')
    cursor = conn.cursor()
    cursor.executemany(
        'INSERT INTO star_people (name, gender, age) VALUES (?, ?, ?)',
        characters
    )
    conn.commit()
    conn.close()
    print("--- %s seconds ---" % (time.time() - start_sinc))