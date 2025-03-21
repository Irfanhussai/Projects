import io
import datetime
import sys
import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from backend.db import fs, documents_collection
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.db import fs, documents_collection

def upload_document(file, uploaded_by, tags):
    file_id = fs.put(io.BytesIO(file.getbuffer()), filename=file.name)
    metadata = {
        "file_id": file_id,
        "filename": file.name,
        "uploaded_by": uploaded_by,
        "upload_date": datetime.datetime.utcnow(),
        "size": file.size,
        "tags": tags.split(",") if tags else []
    }
    documents_collection.insert_one(metadata)
    return "File uploaded successfully!"

def get_documents():
    return list(documents_collection.find({}, {"_id": 0}))
# ////
def list_files():
    """Retrieve all files metadata from GridFS"""
    files = []
    for file in fs.find():
        files.append({
            "filename": file.filename,
            "file_id": str(file._id),  # Convert ObjectId to string
            "upload_date": file.upload_date
        })
    return files
# /////
from pymongo import MongoClient
import gridfs

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["skb_db"]
fs = gridfs.GridFS(db)

def list_files():
    """Retrieve all file metadata from GridFS."""
    files = []
    for file in fs.find():
        files.append({
            "filename": file.filename,
            "file_id": str(file._id),
            "upload_date": file.upload_date
        })
    return files

def get_file(file_name):
    """Retrieve a file's content from GridFS."""
    file = fs.find_one({"filename": file_name})
    if file:
        return file.read()  # Returns binary content
    return None
