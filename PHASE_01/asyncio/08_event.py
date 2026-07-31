import asyncio

async def waiter(event, name):
    print(f"{name} waiting for event to set")
    await event.wait()
    print(f"{name} is set!")

async def setter(event):
    await asyncio.sleep(3)
    print("Setting up event!")
    event.set()

async def main():

    event = asyncio.Event()

    worker1 = asyncio.create_task(waiter(event, "WORKER 1"))
    worker2 = asyncio.create_task(waiter(event, "WORKER 2"))

    setter1 = asyncio.create_task(setter(event))

    await asyncio.gather(worker1, worker2, setter1)
    
    # await worker1
    # await worker2
    # await setter1

asyncio.run(main())


