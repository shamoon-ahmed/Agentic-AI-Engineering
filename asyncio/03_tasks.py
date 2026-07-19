# creating tasks in asyncio
# we use the asyncio.create_task() method when we want to create task manually and to be ran in the background

import asyncio
import time

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

asyncio.run(main())

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

