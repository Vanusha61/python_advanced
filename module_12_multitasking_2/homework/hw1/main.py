import multiprocessing
import sqlite3
import threading

import requests
import time
from multiprocessing import Pool, cpu_count
from multiprocessing.pool import ThreadPool

from queue import Queue

queue_list = Queue()
queue_list_multi = multiprocessing.Queue()

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

def star_people_pool(id:int):
    global queue_list_multi
    try:
        api_star = "https://www.swapi.tech/api/people/{}".format(id)
        response = requests.get(api_star, timeout=30)
        if response.status_code == 200:
            data = response.json()['result']['properties']
            name = data.get('name', "No name")
            gender = data.get('gender', "No gender")
            old = data.get('birth_year', "no birth_year")
            queue_list_multi.put((name, gender, old))
    except Exception as e:
        time.sleep(0.1)

def star_people_thread_pool(id:int):
    try:
        global queue_list
        api_star = "https://www.swapi.tech/api/people/{}".format(id)
        response = requests.get(api_star, timeout=30)
        if response.status_code == 200:
            data = response.json()['result']['properties']
            name = data.get('name', "No name")
            gender = data.get('gender', "No gender")
            old = data.get('birth_year', "no birth_year")
            queue_list.put((name, gender, old))
    except Exception as e:
        time.sleep(0.1)



if __name__ == '__main__':

    start_pool = time.time()
    with Pool(processes=cpu_count()) as pool:
        pool.map(star_people_pool, range(1, 21))
    print("--- %s seconds ---" % (time.time() - start_pool))

    while not queue_list_multi.empty():
        obg = queue_list_multi.get()
        print(obg)

    start_thread_pool = time.time()
    with ThreadPool(processes=cpu_count()) as pool:
        pool.map(star_people_thread_pool, range(1, 21))
    print(time.time()-start_thread_pool)

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
    print("--- %s seconds ---" % (time.time() - start))


    conn = sqlite3.connect('star_people.db')
    cursor = conn.cursor()
    cursor.executemany(
        'INSERT INTO star_people (name, gender, age) VALUES (?, ?, ?)',
        characters
    )
    conn.commit()
    conn.close()


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