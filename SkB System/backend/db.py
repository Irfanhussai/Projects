import pymongo
import redis
import gridfs

# MONGO_URI = "mongodb://localhost:27017/"
# DB_NAME = "skb_db"

# # Initialize MongoDB
# client = pymongo.MongoClient(MONGO_URI)
# db = client[DB_NAME]
# fs = gridfs.GridFS(db)
# users_collection = db["users"]
# documents_collection = db["documents"]

# Initialize Redis
# redis_client = redis.Redis(host="localhost", port=6379, db=0)

from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client["skb_db"]  # Change this to your DB name
users_collection = db["users"]  # Ensure this line exists
documents_collection = db["documents"]
fs = gridfs.GridFS(db)
print("Connected to MongoDB successfully!")
