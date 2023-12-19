#!/usr/bin/env python3
"""This module provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


if __name__ == "__main__":
    """Entry point - returns stats about nginx server"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_coll = client.logs.nginx

    nginx_logs_count = nginx_coll.count_documents({})
    print("{} logs".format(nginx_logs_count))

    http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in http_methods:
        n = nginx_coll.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, n))

    status = nginx_coll.count_documents(
        {"method": "GET", "path": "/status"}
    )

    print("{} status check".format(status))
