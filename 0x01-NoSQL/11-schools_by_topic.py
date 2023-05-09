#!/usr/bin/env python3
""" MongoDB Operations with Python using pymongo """

def schools_by_topic(mongo_collection, topic):
    """ Returns the list of schools having a specific topic.

    Args:
        mongo_collection (pymongo.collection.Collection): The collection of schools.
        topic (str): The topic to filter by.

    Returns:
        list: The list of schools that have the topic in their topics field.
    """
    documents = mongo_collection.find({"topics": topic})
    list_docs = [doc for doc in documents]
    return list_docs
