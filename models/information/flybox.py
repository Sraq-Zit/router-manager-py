import json
import xml.etree.ElementTree as ET
from dataclasses import dataclass

from utils import settings


from .base import InformationBase


@dataclass
class FlyboxInformation(InformationBase):
    """
    Represents the information of a Flybox router.

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
        web_ui_version (str): The web UI (User Interface) version of the router.
        config_file_version (str): The configuration file version of the router.
        cell_id (str): The cell ID of the router.
        cqi (str): The CQI (Channel Quality Indicator) of the router.
        rsrq (str): The RSRQ (Reference Signal Received Quality) of the router.
        rsrp (str): The RSRP (Reference Signal Received Power) of the router.
        rssi (str): The RSSI (Received Signal Strength Indication) of the router.
        sinr (str): The SINR (Signal-to-Interference-plus-Noise Ratio) of the router.
        plmn (str): The PLMN (Public Land Mobile Network) of the router.
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
    web_ui_version: str
    config_file_version: str
    cell_id: str
    cqi: str
    rsrq: str
    rsrp: str
    rssi: str
    sinr: str
    plmn: str    


    def __str__(self):
        """
        Returns a string representation of the FlyboxInformation instance.
        """
        return json.dumps(self.__dict__) if settings.AS_JSON else \
                f"Device Name:                   {self.device_name}\n" \
                f"Serial Number:                 {self.serial_number}\n" \
                f"IMEI:                          {self.imei}\n" \
                f"IMSI:                          {self.imsi}\n" \
                f"Hardware Version:              {self.hardware_version}\n" \
                f"Software Version:              {self.software_version}\n" \
                f"Web UI Version:                {self.web_ui_version}\n" \
                f"Configuration File Version:    {self.config_file_version}\n" \
                f"LAN MAC Address:               {self.lan_mac_address}\n" \
                f"WAN IP Address:                {self.wan_ip_address}\n" \
                f"WAN IPv6 Address:              {self.wan_ipv6_address}\n" \
                f"Cell ID:                       {self.cell_id}\n" \
                f"CQI:                           {self.cqi}\n" \
                f"RSRQ:                          {self.rsrq}\n" \
                f"RSRP:                          {self.rsrp}\n" \
                f"RSSI:                          {self.rssi}\n" \
                f"SINR:                          {self.sinr}\n" \
                f"Wireless Transmit Power:       {self.wireless_transmit_power}\n" \
                f"PLMN:                          {self.plmn}\n" \
                f"Band:                          {self.band}"

    @staticmethod
    def from_xml_string(xml):
        """
        Creates an instance of FlyboxInformation from the given XML string.

        Args:
            xml (str | Element): The XML string/element containing the router information.

        Returns:
            FlyboxInformation: An instance of FlyboxInformation populated with the router information.
        """

        if isinstance(xml, ET.Element):
            root = xml
        else:
            root = ET.fromstring(xml)
        
        device_name = root.find("DeviceName").text if root.find("DeviceName") is not None else ""
        serial_number = root.find("SerialNumber").text if root.find("SerialNumber") is not None else ""
        imei = root.find("Imei").text if root.find("Imei") is not None else ""
        imsi = root.find("Imsi").text if root.find("Imsi") is not None else ""
        hardware_version = root.find("HardwareVersion").text if root.find("HardwareVersion") is not None else ""
        software_version = root.find("SoftwareVersion").text if root.find("SoftwareVersion") is not None else ""
        web_ui_version = root.find("WebUIVersion").text if root.find("WebUIVersion") is not None else ""
        config_file_version = root.find("iniversion").text if root.find("iniversion") is not None else ""
        lan_mac_address = root.find("MacAddress1").text if root.find("MacAddress1") is not None else ""
        wan_ip_address = root.find("WanIPAddress").text if root.find("WanIPAddress") is not None else ""
        wan_ipv6_address = root.find("WanIPv6Address").text if root.find("WanIPv6Address") is not None else ""
        cell_id = root.find("cell_id").text if root.find("cell_id") is not None else ""

        cqi = []
        i = 0
        while root.find(f"cqi{i}") is not None:
            cqi.append(root.find(f"cqi{i}").text)
            i+=1
        cqi = ' '.join(cqi)
        
        rsrq = root.find("rsrq").text if root.find("rsrq") is not None else ""
        rsrp = root.find("rsrp").text if root.find("rsrp") is not None else ""
        rssi = root.find("rssi").text if root.find("rssi") is not None else ""
        sinr = root.find("sinr").text if root.find("sinr") is not None else ""
        wireless_transmit_power = root.find("txpower").text if root.find("txpower") is not None else ""
        plmn = root.find("plmn").text if root.find("plmn") is not None else ""
        band = root.find("band").text if root.find("band") is not None else ""

        return FlyboxInformation(
            device_name=device_name,
            serial_number=serial_number,
            imei=imei,
            imsi=imsi,
            hardware_version=hardware_version,
            software_version=software_version,
            web_ui_version=web_ui_version,
            config_file_version=config_file_version,
            lan_mac_address=lan_mac_address,
            wan_ip_address=wan_ip_address,
            wan_ipv6_address=wan_ipv6_address,
            cell_id=cell_id,
            cqi=cqi,
            rsrq=rsrq,
            rsrp=rsrp,
            rssi=rssi,
            sinr=sinr,
            wireless_transmit_power=wireless_transmit_power,
            plmn=plmn,
            band=band
        )
        