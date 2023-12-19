#!/usr/bin/env python3
"""
This module contains a function that inserts a new document.
"""


def insert_school(mongo_collection, **kwargs):
    """
    This function inserts a new school document into the schools collection.
    """
    return mongo_collection.insert(kwargs)
