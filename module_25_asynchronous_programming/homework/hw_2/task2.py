import requests
from threading import Thread, get_ident
from multiprocessing import Process
import time
import aiohttp
import asyncio

URL = 'http://127.0.0.1:5000/my_test'



def request_url(url):
    res = requests.get(url, timeout=30)
    if res.status_code == 200:
        res = res.content
        file_name = get_ident()
        with open('{}.png'.format(file_name), 'wb') as f:
            f.write(res)


def request_url_proc(url, idx):
    res = requests.get(url, timeout=30)
    if res.status_code == 200:
        res = res.content
        with open('{}.png'.format(idx), 'wb') as f:
            f.write(res)


def my_task_thread():
    start = time.time()
    threads = []
    for _ in range(100):
        thread = Thread(target=request_url, args=(URL,))
        threads.append(thread)
        thread.start()
        time.sleep(0.1)
    for thread in threads:
        thread.join()
    print(time.time() - start)


def my_task_process():
    start = time.time()
    process = []
    for i in range(1, 101):
        proc = Process(target=request_url_proc, args=(URL, i))
        process.append(proc)
        proc.start()
        time.sleep(0.1)

    for proc in process:
        proc.join()
    print(time.time() - start)


def write_file(result, idx: int):
    with open('{}.png'.format(idx), 'wb') as f:
        f.write(result)


async def run_write_task(result, idx):
    return await asyncio.to_thread(write_file, result, idx)


async def my_task_async(client: aiohttp.ClientSession, idx: int):
    async with client.get(URL, timeout=30) as resp:
        if resp.status == 200:
            res = await resp.read()
            await run_write_task(res, idx)


async def start_async():
    async with aiohttp.ClientSession() as client:
        tasks = [my_task_async(client, i) for i in range(1, 101)]
        return await asyncio.gather(*tasks)


if __name__ == '__main__':
    my_task_thread()
    my_task_process()
    start = time.time()
    asyncio.run(start_async())
    print(time.time() - start)
