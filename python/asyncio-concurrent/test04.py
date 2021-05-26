import asyncio
import concurrent

async def inmain():
    print(hash(asyncio.get_event_loop()), hash(asyncio.get_running_loop()))
    for _ in range(5):
        print("Hello")
        await asyncio.sleep(0.5)

def test():
    asyncio.run(inmain())
    return True

async def task():
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        result = await loop.run_in_executor(pool, test)
        print('custom thread pool', result)


async def task2():
    for _ in range(5):
        print("Hello")
        await asyncio.sleep(0.5)

async def main():
    try:
        t = {asyncio.create_task(task2()) for i in range(5)}
        await asyncio.sleep(0.5)
        # asyncio.wait(t)
        # while True:
            # print("hi")
            # await asyncio.sleep(0.5)
    finally:
        print("finally")

try:
    asyncio.run(main())
except (KeyboardInterrupt, SystemExit):
    pass
