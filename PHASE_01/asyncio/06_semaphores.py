# using Semaphores to limit the number of tasks to run concurrently

import asyncio
import time

sem = asyncio.Semaphore(1)

async def download_files(file):
    async with sem:
        print(f"{file} Downloading started...")
        await asyncio.sleep(2)
        print(f"{file} Downloaded")

async def main():
    start = time.time()
    await asyncio.gather(
        download_files("file1"),
        download_files("file2"),
        download_files("file3")
        )
    elapsed = time.time() - start
    print("Elapsed time: ", elapsed)
    
asyncio.run(main())