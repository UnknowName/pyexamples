import asyncio

from aiomultiprocess import Process
import aio_pika


async def provider():
    loop = asyncio.get_event_loop()
    conn = await aio_pika.connect_robust(
        "amqp://guest:siss.rabbit.dev@128.0.100.174",
        loop=loop
    )

    async with conn:
        routing_key = "test_queue"
        channel = await conn.channel()
        await channel.declare_queue(routing_key, durable=True)
        i = 1
        while True:
            i += 1
            try:
                await channel.default_exchange.publish(
                    aio_pika.Message(
                        body='Hello {}'.format(i).encode(),
                        delivery_mode=2
                    ),
                    routing_key=routing_key
                )
            except Exception as e:
                print(e)
            print(i)


async def main():
    for i in range(5):
        p = Process(target=provider)
        p.start()
        # await p.join()


if __name__ == "__main__":
    asyncio.run(main())
