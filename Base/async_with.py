class Async(object):
    def __init__(self):
        print("Init for object async")

    async def _echo(self):
        return "hello,world"

    def __aenter__(self):
        print("enter async aenter.I will execute some prepare work")
        return self._echo()

    async def _exit(self):
        print("I am exit, I will execute some clean works")

    def __aexit__(self, exc_type, exc_val, exc_tb):
        print(exc_type, exc_val, exc_tb)
        return self._exit()


async def echo():
    async with Async() as t:
        print("t is", t)


if __name__ == '__main__':
    import asyncio
    asyncio.run(echo())