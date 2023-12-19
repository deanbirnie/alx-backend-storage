#!/usr/bin/env python3
"""
This module contains a function that updates the topics for a school in the
schools collection.
"""


def update_topics(mongo_collection, name, topics):
    """
    This function changes the topics for a specified document.
    """
    match = { "name": name }
    new_topics = { "$set":
                   { "topics": topics }
    }

    mongo_collection.update_many(match, new_topics)
