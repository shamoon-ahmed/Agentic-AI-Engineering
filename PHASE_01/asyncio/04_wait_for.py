import asyncio
import time

async def fetch_user(id: int) -> dict:
    await asyncio.sleep(2)
    return {"user": id, "name": "shamoon"}

async def main():
    try:
        user = await asyncio.wait_for(fetch_user(2), timeout=2.0)
        print("User: ", user)
    except asyncio.TimeoutError:
        print("Time out error for user")

asyncio.run(main())
