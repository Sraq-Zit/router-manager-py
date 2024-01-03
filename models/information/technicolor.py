

import json
from models.information.base import InformationBase
from utils import settings


class TechnicolorInformation(InformationBase):
    """ Represents the information of a Technicolor router. 
    Attributes:
        device_name (str): The device name.
        serial_number (str): The serial number.
        software_version (str): The software version.
    """

    device_name: str
    serial_number: str
    software_version: str

    def __str__(self):
        """
        Returns a string representation of the FlyboxInformation instance.
        """
        return json.dumps(self.__dict__) if settings.AS_JSON else \
                f"Device Name:                   {self.device_name}\n" \
                f"Serial Number:                 {self.serial_number}\n" \
                f"Software Version:              {self.software_version}\n"