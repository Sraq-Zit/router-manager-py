
from dataclasses import dataclass
import json
from typing import List

import pandas as pd

from models.user_device.base import UserDeviceBase
from utils import settings


@dataclass
class MacFilteringBase():
    """Base class for MacFiltering models."""
    ssid: int
    blacklisted_users: list[UserDeviceBase]
    whitelisted_users: list[UserDeviceBase]

    @staticmethod
    def from_xml():
        """Parse XML response from router."""
        raise NotImplementedError
    
    @property
    def __dict__(self):
        return {
            'ssid': self.ssid,
            'blacklisted_users': [user.__dict__ for user in self.blacklisted_users],
            'whitelisted_users': [user.__dict__ for user in self.whitelisted_users],
        }


class MacFilteringSsidCollection:
    """ Represents a collection of user devices. 

    Attributes:
        devices (list): A list of user devices.
    """

    def __init__(self, ssids=[]):
        self.ssids: List[MacFilteringBase] = ssids

    def display(self):
        """ Display the user devices. """
        if settings.AS_JSON:
            return json.dumps([[ssid.__dict__ for ssid in self.ssids]])

        return "\n\n".join([
            f"SSID: {ssid.ssid}\n"
            f"Blacklisted users:\n"
            + '\n'.join([f"  {user.name}\t {user.mac_address}" for user in ssid.blacklisted_users]) +
            (f"\nWhitelisted users:\n" if len(ssid.whitelisted_users) else "")
            + '\n'.join([f"  {user.name}\t {user.mac_address}" for user in ssid.whitelisted_users])
            for ssid in self.ssids if len(ssid.blacklisted_users) or len(ssid.whitelisted_users)
        ])
