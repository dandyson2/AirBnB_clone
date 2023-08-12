#!/usr/bin/python3

"""Defines the City class."""


from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class City(BaseModel):
    """
    Represent a city.

    Attributes:
        state_id (str): The state id.
        name (str): The name of the city.
    """

    state_id = ""
    name = ""
