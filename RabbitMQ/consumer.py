import asyncio

import aio_pika


async def main(loop):
    try:
        conn = await aio_pika.connect_robust(
            "amqp://guest:siss.rabbit.dev@128.0.100.172", loop=loop
        )
    except Exception as e:
        print(e)
        return
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


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
