#!/usr/bin/python3

"""
This module contains the FileStorage class which is responsible for
serializing instances to a JSON file and deserializing them back to instances.
"""

import json

from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}


class FileStorage:
    """
    The FileStorage class is responsible for
    serializing instances to a JSON file and deserializing them
    back to instances.
    """

    # string - path to the JSON file
    __file_path = "./dev/file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """
        Returns the dictionary __objects.
        """
        if cls:
            new_dict = {}
            for key, value in self.__objects.items():
                if isinstance(value, cls):
                    new_dict[key] = value
            return new_dict

        return self.__objects

    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id.
        """
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path).
        """
        json_dict = {}
        for key, value in self.__objects.items():
            json_dict[key] = value.to_dict()
        with open(self.__file_path, "w") as f:
            json.dump(json_dict, f)

    def reload(self):
        """
        Deserializes the JSON file to __objects.
        """
        try:
            with open(self.__file_path, "r") as f:
                json_dict = json.load(f)
                for key, value in json_dict.items():
                    class_name = value["__class__"]
                    self.__objects[key] = classes[class_name](**value)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it's inside.
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]

    def get(self, cls, id):
        """
        Retrieves an object based on the class and its ID.
        """
        key = "{}.{}".format(cls.__name__, id)
        return self.__objects.get(key, None)

    def count(self, cls=None):
        """
        Returns the count of objects in the file storage matching
        the given class. If no class is passed, it returns the
        count of all objects in the file storage.
        """
        if cls:
            return len(self.all(cls))
        return len(self.__objects)

    def close(self):
        """
        Calls reload() method for deserializing the JSON file to objects.
        """
        self.reload()
