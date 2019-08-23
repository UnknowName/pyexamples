import os

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


def main():
    try:
        client = MongoClient(
            "mongodb://128.0.100.172:27017,128.0.100.173:27017,128.0.100.174:27017/?replicaSet=rs0",
            serverSelectionTimeoutMS=5000,
            readPreference='secondaryPreferred',
        )
        client.admin.command("ismaster")
    except ConnectionFailure:
        client = None
        print("Connect Failed")
        exit(9)
    db = client["siss"]
    user, password = os.getenv("MONGO_USER"), os.getenv("MONGO_PASSWORD")
    db.authenticate(user, password)
    # pprint([attr for attr in dir(db) if not attr.startswith("_")])
    user = db.get_collection("user")
    doc = user.find_one()
    print(doc, doc.get("_id"))


if __name__ == '__main__':
    main()