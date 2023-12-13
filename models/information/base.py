from dataclasses import dataclass
import json

from utils import settings

@dataclass
class InformationBase:
    """
    Represents the information of a router.

    Attributes:
        device_name (str): The device name of the router.
        serial_number (str): The serial number of the router.
        imei (str): The IMEI (International Mobile Equipment Identity) of the router.
        imsi (str): The IMSI (International Mobile Subscriber Identity) of the router.
        hardware_version (str): The hardware version of the router.
        software_version (str): The software version of the router.
        lan_mac_address (str): The LAN (Local Area Network) MAC (Media Access Control) address of the router.
        wan_ip_address (str): The WAN (Wide Area Network) IP (Internet Protocol) address of the router.
        wan_ipv6_address (str): The WAN IPv6 (Internet Protocol version 6) address of the router.
        wireless_transmit_power (str): The wireless transmit power of the router.
        band (str): The band of the router.
    """

    device_name: str
    serial_number: str
    imei: str
    imsi: str
    hardware_version: str
    software_version: str
    lan_mac_address: str
    wan_ip_address: str
    wan_ipv6_address: str
    wireless_transmit_power: str
    band: str

    def __str__(self):
        """
        Returns a string representation of the Information instance.
        """
        return json.dumps(self.__dict__) if settings.AS_JSON else \
                f"Device Name:               {self.device_name}\n" \
                f"Serial Number:             {self.serial_number}\n" \
                f"IMEI:                      {self.imei}\n" \
                f"IMSI:                      {self.imsi}\n" \
                f"Hardware Version:          {self.hardware_version}\n" \
                f"Software Version:          {self.software_version}\n" \
                f"LAN MAC Address:           {self.lan_mac_address}\n" \
                f"WAN IP Address:            {self.wan_ip_address}\n" \
                f"WAN IPv6 Address:          {self.wan_ipv6_address}\n" \
                f"Wireless Transmit Power:   {self.wireless_transmit_power}\n" \
                f"Band:                      {self.band}"
