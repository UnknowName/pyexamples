import os
import asyncio

from aiomultiprocess import Process
import aio_pika


async def provider(flag: int):
    loop = asyncio.get_event_loop()
    """
    _host = os.getenv("RABBITMQ_SERVER")
    _user = os.getenv("RABBITMQ_USER")
    _password = os.getenv("RABBITMQ_PASSWORD")
    """
    _host, _user, _password = "128.0.255.6", "guest", "guest"
    conn_str = "amqp://{user}:{password}@{host}".format(user=_user, host=_host, password=_password)
    conn = await aio_pika.connect_robust(conn_str, loop=loop)

    async with conn:
        routing_key = "test_queue"
        channel = await conn.channel()
        await channel.declare_queue(routing_key, durable=True)
        i = 0
        while True:
            i += 1
            try:
                await channel.default_exchange.publish(
                    aio_pika.Message(
                        body='{}: Hello {}'.format(flag, i).encode(),
                        delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                    ),
                    routing_key=routing_key
                )
                await asyncio.sleep(2)
            except Exception as e:
                print(e)
            print(i)


async def main():
    for i in range(5):
        p = Process(target=provider, args=(i,))
        p.start()
        # await p.join()


if __name__ == "__main__":
    # asyncio.run(main())
    # asyncio.run(provider())
    tasks = [provider(i) for i in range(5)]
    asyncio.run(asyncio.wait(tasks))
