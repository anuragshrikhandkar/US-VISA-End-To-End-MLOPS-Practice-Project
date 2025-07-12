# # test_mongo.py
# import pymongo
# import os
# from dotenv import load_dotenv

# load_dotenv()  # Load environment variables from .env file if present

# MONGODB_URL = os.getenv("MONGODB_URL")
# client = pymongo.MongoClient(MONGODB_URL)

# # ✅ Use correct and valid DB and collection names
# db_name = "US_VISA"              # ✅ No dot!
# collection_name = "visa_data"    # ✅ collection inside this DB

# # Connect to database and collection
# db = client[db_name]
# collection = db[collection_name]

# # Count documents in the collection
# count = collection.count_documents({})
# print(f"📦 Documents in collection '{collection_name}':", count)

# # Show a few sample documents
# docs = list(collection.find().limit(2))
# for doc in docs:
#     print(doc)

import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
client = pymongo.MongoClient(MONGODB_URL)

print("📁 Scanning MongoDB databases and collections...")
for db_name in client.list_database_names():
    db = client[db_name]
    print(f"\n🗃️ Database: {db_name}")
    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        count = collection.count_documents({})
        print(f"   📂 Collection: {collection_name} ➜ {count} documents")