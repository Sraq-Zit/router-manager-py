
from dataclasses import dataclass
import json
from typing import List

import pandas as pd

from utils import settings


@dataclass
class UserDeviceBase:
    """ Represents the base of a user device. 
    
    Attributes:
        name (str): The name of the device.
        ip_address (str): The IP (Internet Protocol) address of the device.
        mac_address (str): The MAC (Media Access Control) address of the device.
        interface (str): The interface of the device.
        uptime (int): The uptime of the device.
        active (bool): True if the device is active, False otherwise.
    """

    name: str
    ip_address: str
    mac_address: str
    interface: str
    uptime: int
    active: bool
    is_local: bool



class UserDeviceBaseCollection:
    """ Represents a collection of user devices. 
    
    Attributes:
        devices (list): A list of user devices.
    """
    def __init__(self, devices=[]):
        self.devices: List[UserDeviceBase] = devices

    def display_as_dataframe(self, devices=None):
        """ Display the user devices as a DataFrame. """

        devices_sorted = devices or sorted(self.devices, key=lambda d: d.active)
        data = {
            'Name': [d.name for d in devices_sorted],
            'Active': ['✓' if d.active else 'x' for d in devices_sorted],
            'Interface': [d.interface for d in devices_sorted],
            # 'Uptime': [d.uptime for d in devices_sorted],
            'IP Address': [d.ip_address.split(';')[0] if d.ip_address else '' for d in devices_sorted],
            'MAC Address': [d.mac_address for d in devices_sorted],
        }

        return pd.DataFrame(data=data)
    
    def display_active_as_dataframe(self):
        """ Display the active user devices as a DataFrame. """
        return self.display_as_dataframe(self.display_active_as_json())
    
    def display_inactive_as_dataframe(self):
        """ Display the inactive user devices as a DataFrame. """
        return self.display_as_dataframe(self.display_inactive_as_json())
    
    def display_active_as_json(self):
        """ Display the active user devices as JSON. """
        return [d for d in self.devices if d.active]
    
    def display_inactive_as_json(self):
        """ Display the inactive user devices as JSON. """
        return [d for d in self.devices if not d.active]
    
    def display_active(self):
        """ Display the active user devices. """
        return self.display_active_as_json() if settings.AS_JSON else self.display_active_as_dataframe()
    
    def display_inactive(self):
        """ Display the inactive user devices. """
        return self.display_inactive_as_json() if settings.AS_JSON else self.display_inactive_as_dataframe()
        
    def display(self, include_inactive=False):
        """ Display the user devices. """
        devices = [d for d in self.devices if include_inactive or d.active]
        if settings.AS_JSON:
            return json.dumps([d.__dict__ for d in devices])
        
        if include_inactive:
            return self.display_inactive_as_dataframe().__repr__() \
                + '\n\nActive devices:\n' \
                + self.display_active_as_dataframe().__repr__()