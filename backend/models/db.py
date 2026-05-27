from pymongo import MongoClient
from config.config import MONGO_URI

try:

    client = MongoClient(MONGO_URI)

    # Test MongoDB connection
    client.admin.command('ping')

    print("MongoDB Atlas Connected Successfully")

    db = client["fake_news_db"]

    users_collection = db["users"]

    history_collection = db["history"]

except Exception as e:

    print("MongoDB Connection Error:", e)