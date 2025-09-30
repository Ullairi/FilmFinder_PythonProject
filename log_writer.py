from mongo_connector import MongoConnector
from datetime import datetime


class LogWriter:
    """Save search results/logs to MongoDB database"""

    def __init__(self):
        self.mongo = MongoConnector()

    def search_log(self, search_type: str, params: dict, films_found: int, more_info: str = ""):
        """
        Save search results to MongoDB

        :param search_type:
        :param params: Dictionary of used search parameters
        :param results_count: Number of search results returned by search
        :return: None
        """

        log_entry = {
            "timestamp": datetime.now(),
            "search_type": search_type,
            "params": params,
            "films_found": films_found,
            "more_info": more_info
        }
        self.mongo.save_log(log_entry)