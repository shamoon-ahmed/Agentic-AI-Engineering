# Synchronization in Async Code

import asyncio

counter = 0
lock = asyncio.Lock()

"""async def count(name):
    global counter
    for _ in range(100):
        temp = counter
        await asyncio.sleep(0.001)
        counter = temp + 1
    print(name, "done")"""

async def count(name):
    global counter
    for _ in range(100): # critical section
        async with lock: 
            temp = counter
            await asyncio.sleep(0.001)
            counter = temp + 1
    print(name, "done")

async def main():
    await asyncio.gather(count("Task1"), count("Task2"))
    print("Final Value: ", counter)

asyncio.run(main())

'''
the expected output of this code should be 200 but we get 100 and the reason is that, 
when task1 runs, it sees the counter = 0, temp = 0, and when it reaches asyncio.sleep(0.001), 
the event loops runs task2 in that small time and task2 again sees counter = 0, temp = 0 because
task1 never updated counter = temp + 1 as it was paused at asyncio.sleep(0.001) and never reached ahead.
now back to task2, now that it is paused again at asyncio.sleep(0.001) and it also didnt update counter = temp + 1,
so event loop now resumes task1 from counter = temp + 1. now the counter value updates and event loop resumes task2
which still has the old temp value = 0, when it updates the counter = temp + 1, it becomes 1, just like what task1 did,
so both tasks, repeats the increment number which makes it 100 at the end instead of 200 

this is a Race Condition when two tasks update the same value/variable/object

to fix this, so that two tasks can't update the same variabl/object simultaneously, we lock that section 
and that section is called Critical Section. now we get output 200 because task1 updates the counter then task2 takes turn
'''