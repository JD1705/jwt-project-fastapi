"""
module: database.py
purpose: store database configuration and connections
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri)
db = client["auth_jwt_project"]

def get_collection(collection_name: str):
    collection = db[collection_name]

    return collection
