#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from os import environ

if environ.get('HBNB_TYPE_STORAGE') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()

class_dict = {
    "Amenity": "amenity",
    "BaseModel": "base_model",
    "City": "city",
    "Place": "place",
    "Review": "review",
    "State": "state",
    "User": "user"
}
