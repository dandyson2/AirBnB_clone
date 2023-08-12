#!/usr/bin/python3

"""Defines the Amenity class."""


from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class Amenity(BaseModel):
    """Represent an amenity.

    Attributes:
        name (str): The name of the amenity.
    """

    name = ""
