import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

START_URL = 'https://nplus1.ru/'
MAX_DEPTH = 3


def parse_links(html: str, base_url: str) -> set:
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        full = urljoin(base_url, href)
        if full.startswith(('http://', 'https://')):
            links.add(full)
    return links


async def fetch(session, url):
    try:
        async with session.get(url, timeout=30) as resp:
            if resp.status != 200:
                return None
            return await resp.text()
    except Exception:
        return None


async def main():
    async with aiohttp.ClientSession() as session:
        visited = {START_URL}
        current_urls = {START_URL}
        all_links = set()

        for depth in range(MAX_DEPTH + 1):
            print(f"Глубина {depth}: обрабатываем {len(current_urls)} страниц...")

            tasks = [fetch(session, url) for url in current_urls]
            htmls = await asyncio.gather(*tasks)

            new_links = set()
            for html, base_url in zip(htmls, current_urls):
                if html is not None:
                    links = parse_links(html, base_url)
                    new_links.update(links)

            all_links.update(new_links)
            current_urls = new_links - visited
            visited.update(current_urls)

            if not current_urls:
                break

        print(f"Всего собрано ссылок: {len(all_links)}")

        with open('crawled_links.txt', 'w', encoding='utf-8') as f:
            for link in all_links:
                f.write(link + '\n')
        print("Ссылки сохранены в crawled_links.txt")


if __name__ == '__main__':
    asyncio.run(main())
