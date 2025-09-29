from mongo_connector import MongoConnector
from datetime import datetime


class LogStats:
    """Class to analyze search results/logs stored in MongoDB database"""

    def __init__(self):
        self.mongo = MongoConnector()
        self.collection = self.mongo.get_collection()

    def top_queries(self, limit=5):
        """
        Get top 5 queries stored in MongoDB database by params

        :param limit:  how much results to return
        :return: list of popular queries stored in MongoDB database
        """

        mongo_query = [
            {"$group": {
                "_id": {"search_type": "$search_type", "params": "$params", "other_info": "$other_info"},
                "results_count": {"$sum": "$result"},
                "latest": {"$max": "$timestamp"}
            }},
            {"$sort": {"results_count": -1, "latest": -1}},
            {"$limit": limit}
        ]
        return list(self.collection.aggregate(mongo_query))

    def last_queries(self, limit=5):
        """
        Get last 5 queries stored in MongoDB database by params
        :param limit:  how much results to return
        :return: List of last queries stored in MongoDB database
        """

        mongo_query = [
            {"$sort": {"timestamp": -1}},
            {"$limit": limit}
        ]
        return list(self.collection.aggregate(mongo_query))

    def queries_output(self, queries):
        """Printing queries in a readable and user-friendly format"""
        for query in queries: # Handles both top 5 queries and last 5 queries
            if "_id" in query and isinstance(query["_id"], dict):
                search_type = query["_id"].get("search_type", "Unknown")
                params = query["_id"].get("params", {})
                more_info = query["_id"].get("other_info", "")
                count = query.get("results_count", 1)
                latest = query.get("latest")
            else:
                search_type = query.get("search_type", "Unknown")
                params = query.get("params", {})
                more_info = query.get("other_info", "")
                count = query.get("result", 1)
                latest = query.get("timestamp")

            latest_str = latest.strftime("%Y-%m-%d %H:%M") if latest else "N/A"

            if search_type.lower() == "keyword":
                print(f"Keyword search: {params.get('keyword')} | Results: {count} | Latest: {latest_str}")
            elif search_type.lower() == "genre":
                info = more_info or f"Category {params.get('category_id', '')}, Years {params.get('min_year', '')}-{params.get('max_year', '')}"
                print(f"Genre search: {info} | Results: {count} | Latest: {latest_str}")
            else:
                print(f"{search_type} search: {params} | Results: {count} | Latest: {latest_str}")