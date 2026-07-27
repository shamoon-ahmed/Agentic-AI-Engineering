import asyncio
import time

def fetch(t):
    time.sleep(t)
    print("Fetched in", t)

async def main():

    task1 = asyncio.create_task(asyncio.to_thread(fetch, 2))
    task2 = asyncio.create_task(asyncio.to_thread(fetch, 3))

    await task1
    print("Task1 completed")

    await task2
    print("Tssk2 completed")

asyncio.run(main())

"""
if there's a function or library that couldn't be awaited or the async feature is not supported,
we can wrap it around the threads and it will work like async code
"""