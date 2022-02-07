#!/usr/bin/env python3

import asyncio

def inside_func():
    asyncio.create_task(async_task())

async def async_task():
    print("hi")

async def main():
    inside_func()
    await asyncio.sleep(1)

asyncio.run(main())
