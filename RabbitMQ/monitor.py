import json

import aiohttp


class RabbitMQ(object):
    def __init__(self, host: str, user: str, password: str):
        self._host = host
        self._auth = aiohttp.BasicAuth(login=user, password=password, encoding="utf8")

    async def get_attr(self, attr_name):
        _api = "http://{}:15672/api/{}".format(self._host, attr_name)
        async with aiohttp.ClientSession(auth=self._auth, timeout=aiohttp.ClientTimeout(5)) as session:
            async with session.get(_api) as resp:
                if resp.status == 200:
                    _resp = await resp.text()
                    channels = json.loads(_resp)
                    print(len(channels))
                else:
                    print(await resp.text())


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    client = RabbitMQ("128.0.255.6", "guest", "guest")
    loop.run_until_complete(client.get_attr("channels"))
    loop.close()
