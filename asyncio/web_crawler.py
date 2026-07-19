import asyncio
from typing import List
import random
import time


class AsyncWebCrawler:
    def __init__(self, max_concurrent: int = 10, max_depth: int = 3):
        self.max_concurrent = max_concurrent    # Cuncurrency level
        self.max_depth = max_depth              # Depth
        self.visited = set()                    # URLs visited
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.results = []                       # URLs processed


    async def fetch_page(self, url: str) -> List[str]:
        wait_prd = random.uniform(.3, 2)
        print(f"{url} - await asyncio.sleep({wait_prd})")  # Info - Sleep time of each URL
        await asyncio.sleep(wait_prd)  # Simulates page fetch
        num_links = random.randint(2, 5)  # Simulate finding 2-5 links
        links = [f"{url}/page{i}" for i in range(num_links)]
        return links


    async def crawl_url(self, url: str, depth: int):
        if depth > self.max_depth:
            return
        if url in self.visited:
            return

        self.visited.add(url)
        print(f"  {'  ' * depth}🕷️  Crawling: {url} (depth: {depth})")

        try:
            tasks = []
            # ✅ Semaphore ONLY around fetch - release immediately
            async with self.semaphore:
                links = await asyncio.wait_for(self.fetch_page(url), timeout=1.5)

            self.results.append({"url": url, "depth": depth, "links_found": len(links)})

            # Spawn children (parent no longer holds semaphore)
            if depth < self.max_depth:
                for link in links:
                    if link not in self.visited:
                        tasks.append(self.crawl_url(link, depth + 1))
            if tasks:
                print(f"Queuing {len(tasks)} more tasks")
                await asyncio.gather(*tasks, return_exceptions=True)

        except asyncio.TimeoutError:
            print(f"  {'  ' * depth}⚠️  Timeout: {url}")
        except Exception as e:
            print(f"  {'  ' * depth}❌ Error crawling {url}: {e}")

    async def crawl(self, start_url: str):
        await self.crawl_url(start_url, depth=0)


async def crawl_sites():
    crawler = AsyncWebCrawler(max_concurrent=5, max_depth=2)

    start_url = "https://example.com"
    print(f"Starting crawl from: {start_url}\n")

    start = time.time()
    await crawler.crawl(start_url)
    elapsed = time.time() - start

    print(f"\n✅ Crawl completed in {elapsed:.2f}s")
    print(f"   Pages visited: {len(crawler.visited)}")
    print(f"   Pages processed: {len(crawler.results)}")
    for result in crawler.results:
        print(result)


asyncio.run(crawl_sites())