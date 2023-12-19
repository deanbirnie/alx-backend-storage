#!/usr/bin/env python3
"""This module contains a function that searches for all entries with a given topic"""


def schools_by_topic(mongo_collection, topic):
    """This function searches for a specific topic on each document"""
    documents = mongo_collection.find({"topics": topic})
    return list(documents)
