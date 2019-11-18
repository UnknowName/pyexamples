import os
import asyncio

import aio_pika


async def main(loop):
    """
    _host = os.getenv("RABBITMQ_SERVER")
    _user = os.getenv("RABBITMQ_USER")
    _password = os.getenv("RABBITMQ_PASSWORD")
    """
    _host, _user, _password = "128.0.100.170", "guest", "guest"
    conn_str = "amqp://{user}:{password}@{host}".format(user=_user, host=_host, password=_password)

    try:
        conn = await aio_pika.connect_robust(conn_str, loop=loop)
    except Exception as e:
        print(e)
        exit(2)
    async with conn:
        queue_name = "test_queue"
        channel = await conn.channel()
        queue = await channel.declare_queue(
            queue_name,
            durable=True,
            auto_delete=False
        )

        async with queue.iterator() as queue_iter:
            # Cancel consuming after __aexit__
            async for message in queue_iter:
                async with message.process():
                    print(message.body)
                    if queue.name in message.body.decode():
                        print(queue.name)
                        break
                    await asyncio.sleep(0.1)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
