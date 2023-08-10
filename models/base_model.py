#!/urs/bin/python3

"""Defines the BaseModel class."""


import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Represents the BaseModel of the AirBnB project."""
    def __init__(self, *args, **kwargs):
        """
        This initializes instance attributes
        Args:
            - *args: list of arguments
            - **kwargs: dict of key-values arguments
        """

        if kwargs is not None and kwargs != {}:
            for key in kwargs:
                if key == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[key] = kwargs[key]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """Define the string and its return values of data type"""
        class_name = self.__class__.__name__
        return ("[{}] ({}) {}".format(class_name, self.id, self.__dict__))

    def save(self):
        """Updates the public instance attribute
        updated_at with the current datetime"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Returns a dictionary containing all
        keys/values of __dict__ of the instance"""
        subjet_dict = self.__dict__.copy()
        subject_dict["__class__"] = self.__class__.__name__
        subject_dict["created_at"] = subject_dict["created_at"].isoformat()
        subject_dict["updated_at"] = subject_dict["updated_at"].isoformat()
        return (subject_dict)
