# let us run multiple coroutines at once

import asyncio
import time

async def greet(name): # this is also called a coroutine
    print("Started greeting!")
    await asyncio.sleep(2)
    print("GM ", name)

async def main():
    start_time = time.time()
    await asyncio.gather(greet("shamoon"), greet("shahmir"), greet("shania"))
    elapsed_time = time.time() - start_time
    print("elapsed time: ", elapsed_time)

asyncio.run(main())