import os
import dotenv
from pathlib import Path
from pymongo import MongoClient

dotenv.load_dotenv(Path('.env'))

class MongoConnector:
    """Connect class to MongoDB database"""

    def __init__(self):
        """
        Initialize MongoDB client and access database and collection

        Take connection info from environment variables:
        MONGO_URL
        MONGO_DB
        MONGO_COLLECTION
        """
        self.mongo_url = os.environ.get("MONGO_URL")
        self.database_name = os.environ.get("MONGO_DB")
        self.collection_name = os.environ.get("MONGO_COLLECTION")

        self.client = MongoClient(self.mongo_url)
        self.db = self.client[self.database_name]
        self.collection = self.db[self.collection_name]


    def save_log(self, log_entry:dict):
        """
        Save a log entry into collection
        :param log_entry: Log entry to be saved
        :return: Insert one result from pymongo
        """
        return self.collection.insert_one(log_entry)

    def get_collection(self):
        """
        Return mongo collection for direct operation

        :return: pymongo collection
        """
        return self.collection