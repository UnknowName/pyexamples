import aiohttp

from pyquery import PyQuery


class UserAgent(object):
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36"
                      "(KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"
    }

    def __init__(self, splash: str = ""):
        self.splash = splash if splash.startswith("http://") else "http://{}".format(splash)

    async def get(self, url: str):
        if self.splash:
            _url_fmt = "{}/render.html?url={}&wait=2&images=0"
            url = _url_fmt.format(self.splash, url)
        async with aiohttp.ClientSession(headers=self.HEADERS) as session:
            async with session.get(url) as resp:
                response = await resp.text()
                js = PyQuery(response)
                # 取出当前活动商品的列表
                actives = js("ul.active li")
                for active_goods in actives:
                    pq_goods = PyQuery(active_goods)
                    price = await get_attr(pq_goods, "price")
                    name = await get_attr(pq_goods, "name")
                    print(name)
                    print(await split_price(price))


async def get_attr(q: PyQuery, attr_name: str) -> str:
    attr = ".{}".format(attr_name)
    return q(attr).text()


async def split_price(price: str):
    return [s.strip('元') for s in price.split('\n')]


if __name__ == '__main__':
    import asyncio
    agent = UserAgent("http://128.0.255.6:8050")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(agent.get("https://www.mi.com/seckill"))
    loop.close()
