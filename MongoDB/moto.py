import os

from motor.motor_asyncio import AsyncIOMotorClient


async def main():
    try:
        user, password = os.getenv("MONGO_USER"), os.getenv("MONGO_PASSWORD")
        client = AsyncIOMotorClient(
            f"mongodb://{user}:{password}@128.0.100.172,128.0.100.173,128.0.100.174/siss?replicaSet=rs0",
            serverSelectionTimeoutMS=5000,
            readPreference='secondaryPreferred',
        )
        await client.admin.command("ismaster")
    except Exception as e:
        client = None
        print("Error: ", e)
        exit(9)
    print("Connect MongoDB Replication Set Successful")
    # Query document
    collect = client["siss"]["user"]
    some_user = await collect.find_one()
    print(some_user)
    # Query many
    async for doc in collect.find({}).sort("_id"):
        print(doc)
    # Insert One
    add_user = dict(_id="12", name="chengjn", _class="cn.com.siss.mongo.entity.User", email="burrt@sina.com")
    result = await collect.insert_one(add_user)
    print(result.inserted_id)
    # Insert Many
    users = [dict(_id=str(i), name="cheng" + str(i), _class="cn.com.siss") for i in range(20, 100)]
    results = await collect.insert_many(users)
    print(results)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
