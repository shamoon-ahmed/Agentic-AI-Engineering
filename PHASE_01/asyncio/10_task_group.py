"""
a modern way of executing multipl coroutines in a group

You use tg.create_task() to schedule coroutines inside the group. 
You can retrieve their return values by calling .result() on the task objects after the block exits safely.

"""

import asyncio

async def fetch_data(t):
    await asyncio.sleep(t)
    print(f"Fetched data for {t}...")

async def main():

    async with asyncio.TaskGroup() as tg:
        results = [tg.create_task(fetch_data(i)) for i in range(1, 3)]

    print(f"Results: {[result.result for result in results]}")

    return "Main corutine done"

result = asyncio.run(main())
print(result)