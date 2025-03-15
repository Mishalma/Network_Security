import pymongo
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(f"Connecting to: {MONGO_DB_URL}")

try:
    client = pymongo.MongoClient(MONGO_DB_URL)
    db = client["MISHALAI"]
    collection = db["Network_Data"]  # Ensure this matches
    print("Connection successful!")
    documents = list(collection.find().limit(5))
    if documents:
        print(f"Fetched {len(documents)} records: {documents}")
    else:
        print("No data found in the collection.")
    client.close()
except Exception as e:
    print(f"Connection failed: {e}")