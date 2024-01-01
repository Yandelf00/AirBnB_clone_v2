#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
import os


class FileStorage:
    """This class serializes instances to a JSON file and
    deserializes JSON file to instances
    Attributes:
        __file_path: path to the JSON file
        __objects: objects will be stored
    """
    __file_path = 'file.json'
    __objects = {}

    def classes(self):
        """Returns a dictionary of valid classes and their references."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
        }
        return classes

    def delete(self, obj=None):
        """loop through __objects, compare each value
        of key with cls argument which is object
        """
        if obj:
            id = obj.to_dict()["id"]
            className = obj.to_dict()["__class__"]
            keyName = className+"."+id
            if keyName in FileStorage.__objects:
                del (FileStorage.__objects[keyName])
                self.save()

    def all(self, cls=None):
        """Returns a dictionary of models in storage"""
        print_dict = {}
        if cls:
            className = cls.__name__
            for k, v in FileStorage.__objects.items():
                if k.split('.')[0] == className:
                    print_dict[k] = v
            return print_dict
        else:
            return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """ Serializes __objects to the JSON file """
        Serialize_dict = {}

        for key, value in FileStorage.__objects.items():
            Serialize_dict[key] = value.to_dict()

        with open(FileStorage.__file_path, 'w') as file:
            json.dump(Serialize_dict, file)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    cls_name = key.split('.')[0]
                    if cls_name in self.classes():
                        instance = self.classes()[cls_name](**val)
                        self.new(instance)
        except FileNotFoundError:
            pass

    def close(self):
        """method for deserializing the JSON file to objects"""
        self.reload()
