from dataclasses import dataclass
import json

from utils import settings

@dataclass
class InformationBase:
    """ Represents the information of a router. """

    def __str__(self):
        """
        Returns a string representation of the Information instance.
        """
        raise NotImplementedError()
