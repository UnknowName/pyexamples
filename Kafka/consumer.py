import asyncio

import aiokafka


async def main():
    loop = asyncio.get_event_loop()
    consumer = aiokafka.AIOKafkaConsumer(
        "my_topic4",
        loop=loop,
        bootstrap_servers="128.0.255.10:9092",
        # Consumer must be in a group to commit
        group_id="test",
        # Autocommit every second
        auto_commit_interval_ms=1000,
        # If committed offset not found, start from begin
        auto_offset_reset="earliest"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(
                "{}:{:d}:{:d}: key={} value={} timestamp_ms={}".format(
                    msg.topic, msg.partition, msg.offset, msg.key, msg.value,
                    msg.timestamp)
            )
    finally:
        await consumer.stop()


if __name__ == '__main__':
    asyncio.run(main())
