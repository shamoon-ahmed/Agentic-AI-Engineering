# creating tasks in asyncio
# we use the asyncio.create_task() method when we want to create task manually and to be ran in the background

import asyncio
import time
from turtle import down

async def download(url): # coroutine
    print(f"Download started for {url}...")
    await asyncio.sleep(2)
    print(f"Download finished for {url}!")

async def main():

    # creating task of the coroutine
    task1 = asyncio.create_task(download("site1"))
    task2 = asyncio.create_task(download("site2"))

    print("Tasks Started!")
    start = time.time()

    # await download("site1")
    # await download("site2")

    await task1
    await task2

    print("Tasks finished!")
    elapsed = time.time() - start
    print(elapsed)

# asyncio.run(main())

''' 
what happens here:
1. the actual runnable line is the 'asyncio.run(main())' which executes
2. main() runs and event loop takes control. It comes to task1 and schedules it in the background. same for task2
3. prints "Task Started!"
4. at await, it pauses main() until task1 is done (as task1 is already scheduled)
5. when it runs task1, it prints "Download started for site1"
6. as it reaches await asyncio.sleep(2), it pauses task1 for 2 secs 
   but insead of sitting idle, it runs the other scheduled task (task2) 
   which follows the same process until it reaches await asyncio.sleep(2) and task2 is also paused now
7. in a bigger picture, main(), task1, and task2 are all paused, as soon as 2 secs expires,
   the event loop sees that the first task paused was task1, so it resumes and prints "Finished download for site1"
   same for task2
8. as both tasks are finished now, the event loop resumes main() which then prints "Task Finished"
9. The event loop ends here

the behaviour is a little different when we await a coroutine or a task.
when we await a task, it gives control back to event loop like when in task1, when it comes to asyncio.sleep(2), 
it gives control back to event loop which helps event loop to execute the other scheduled tasks.
BUT when we await a coroutine (means directly the download function we made), and when it comes to asyncio.sleep(2),
it doesnt give control back to event loop which keeps it stuck for 2 seconds, executes the whole function first then
comes to other coroutine

'''

# what if we await the task2 first and then task1

async def main2():

    task1 = asyncio.create_task(download("site1"))
    task2 = asyncio.create_task(download("site2"))

    result1 = await task2
    print(f"{result1}, Task2 completed")

    result2 = await task1
    print(f"{result2}, Task1 completed")

asyncio.run(main2())

'''
notice, this is the output:

Download started for site1...
Download started for site2...
Download finished for site1!
Download finished for site2!
None, Task2 completed
None, Task1 completed

even tho we awaited task2 first, the download started from site1, then site2, finished for site1 then site2
but at the end Task2 completed printed then Task1

the reason is, await doesnt guarantee the execution of the awaited statement at that exact moment
the event loop just executes whichever job is ready and as event loop follow FIFO method,
the first task scheduled (task1) was executed first
but as task2 was awaited first, the event loop waited until task2 was completed
once it was completed, it printed Task2 completed then Task1 completed printed

'''