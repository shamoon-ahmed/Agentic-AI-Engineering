import asyncio
import random

async def producer(queue):
    for i in range(10):
        item = f"Task {i}"
        await asyncio.sleep(random.uniform(0.2, 0.5))
        await queue.put(item)
        print(f"{item} added to job")

async def consumer(queue, name):
    while True:
        item = await queue.get()
        print(f"Consumer {name} consumed {item}")
        await asyncio.sleep(random.uniform(0.2, 0.5))
        queue.task_done()

async def main():
    queue = asyncio.Queue()

    producer1 = asyncio.create_task(producer(queue))
    consumer1 = asyncio.create_task(consumer(queue, "Q1"))
    consumer2 = asyncio.create_task(consumer(queue, "Q2"))

    await producer1
    await queue.join()

    consumer1.cancel()
    consumer2.cancel()

asyncio.run(main())

"""
so basically what happens here is:
suppose we're making instagram. user uploads image which first gets saved then resized, then a thumbnail is made, etc etc.
if we do all of this and then get back to the user, the UX would be so bad. 
so instead we introduced the concept of producer and consumer
the queue follow FIFO method. the producer and consumer uses queue
the producer adds the job to the queue, thats it.
the consumer sees if there's a job in the queue and then processes it.
so back to the instagram example, instead of making the user wait until everything processes, we tell them that 
their image is uploaded and its in processing to make it in the correct format for the app
the producer gets that image uploading job and adds in the queue, the app tells user that the image is saved/uploaded. 
now when consumer sees this, it takes that job from the queue and processes it.

its better to make 2-3-4 consumers as if a new user wants to do something, that job can be handled by other consumer tasks
as the code is async, the tasks will switch between each other depending on whos waiting for the job

"""