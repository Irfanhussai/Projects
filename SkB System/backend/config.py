from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

SECRET_KEY = os.getenv("SECRET_KEY", "fallback_default_key")
