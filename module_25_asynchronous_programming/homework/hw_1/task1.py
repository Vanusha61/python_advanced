import asyncio
from pathlib import Path

import aiohttp

URL = 'https://cataas.com/cat'

# *если у вас не выполняются запросы к этому API, то вы можете подобрать любой другой API с изображениями, найти его можно например в этом перечне:
# https://github.com/public-apis/public-apis#animals

CATS_WE_WANT = 10
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()


async def get_cat(client: aiohttp.ClientSession, idx: int) -> bytes:
    async with client.get(URL) as response:
        print(response.status)
        result = await response.read()
        await run_write(result, idx)


# async def write_to_disk(content: bytes, id: int):
#     file_path = "{}/{}.png".format(OUT_PATH, id)
#     async with aiofiles.open(file_path, mode='wb') as f:
#         await f.write(content)

def write_to_disk(file_path: str, result: bytes, idx: int) -> None:
    with open(file_path, 'wb') as f:
        f.write(result)


async def run_write(result: bytes, idx: int) -> None:
    file_path = "{}/{}.png".format(OUT_PATH, idx)
    return await asyncio.to_thread(write_to_disk, file_path, result, idx)


async def get_all_cats():
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(15)) as client:
        tasks = [get_cat(client, i) for i in range(CATS_WE_WANT)]
        return await asyncio.gather(*tasks)


def main():
    res = asyncio.run(get_all_cats())
    print(len(res))


if __name__ == '__main__':
    main()
