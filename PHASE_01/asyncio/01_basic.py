# basic code of asyncio where it takes 2 secs to complete

import asyncio
import time

async def main():
    print("Starting...")
    await asyncio.sleep(2)
    print("Ended")

asyncio.run(main())