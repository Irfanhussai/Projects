# from backend.db import documents_collection
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.db import documents_collection

def search_documents(query, file_type, start_date, end_date):
    search_query = {"$or": [{"filename": {"$regex": query, "$options": "i"}}]}
    if file_type:
        search_query["fileType"] = file_type.lower()
    if start_date and end_date:
        search_query["upload_date"] = {"$gte": start_date, "$lte": end_date}
    
    return list(documents_collection.find(search_query, {"_id": 0}))
