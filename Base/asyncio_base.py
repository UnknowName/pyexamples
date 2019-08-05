import time
import asyncio


async def echo(what: str, deply: int) -> None:
    print(time.time())
    await asyncio.sleep(deply)
    print(what)
    return None


async def main_concurrent():
    print("start main_concurrent ", time.time())
    # coroutine will concurrently must wrapped by Task object
    task1 = asyncio.create_task(echo("hello", 2))
    task2 = asyncio.create_task(echo("world", 3))
    await task1
    await task2
    print("end main_concurrent ", time.time())


async def main_corotinue():
    print("start main_corotinue ", time.time())
    await echo("hello2", 2)
    await echo("world2", 3)
    print("end main_corotinue ", time.time())


if __name__ == '__main__':
    # Total 3 second
    asyncio.run(main_concurrent())
    # Total 5 second
    asyncio.run(main_corotinue())
    # Total also  use 5 second
    # main_corotinue and main_concurrent concurrent run
    loop = asyncio.get_event_loop()
    tasks = [main_corotinue(), main_concurrent()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


