import bcrypt
import jwt
import datetime

import sys
import os

# Add project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.db import users_collection  # Example import


# from backend.db import users_collection
# from db import users_collection
# from backend.config import SECRET_KEY
from backend.config import SECRET_KEY

def register_user(username, password, role):
    if users_collection.find_one({"username": username}):
        return "User already exists"
    
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    users_collection.insert_one({"username": username, "password": hashed_password, "role": role})
    return "User registered successfully!"

def login_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        payload = {
            "username": username,
            "role": user["role"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token
    return None

def verify_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
