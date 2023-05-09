#!/usr/bin/env python3
"""This module contains a function that queries a MongoDB collection
and returns the students sorted by their average score using pymongo."""

from typing import List
from pymongo.collection import Collection


def top_students(mongo_collection: Collection) -> List[dict]:
    """Returns all students sorted by average score.

    Args:
        mongo_collection (Collection): The MongoDB collection to query.

    Returns:
        List[dict]: A list of dictionaries representing the students and their average scores.

    Raises:
        TypeError: If mongo_collection is not a Collection object.
    """
    if not isinstance(mongo_collection, Collection):
        raise TypeError("mongo_collection must be a Collection object")

    students = mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ])
    return list(students)
