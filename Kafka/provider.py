import asyncio

import aiokafka


async def main():
    loop = asyncio.get_event_loop()
    producer = aiokafka.AIOKafkaProducer(
        loop=loop,
        bootstrap_servers='128.0.255.10:9092'
    )
    await producer.start()
    try:
        result = await producer.send_and_wait("my_topic", key=b"test", value=b"hello,world!")
        print(result)
        print(result.offset)
    finally:
        await producer.stop()


if __name__ == '__main__':
    asyncio.run(main())
