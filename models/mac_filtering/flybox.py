from dataclasses import dataclass
import xml.etree.ElementTree as ET


from models.mac_filtering.base import MacFilteringBase
from models.user_device.base import UserDeviceBase

@dataclass
class MacFilteringFlybox(MacFilteringBase):
    """MacFiltering class for Flybox."""
    
    @staticmethod
    def from_xml(ssid: ET.Element):
        """Parse XML response from router."""

        table = MacFilteringFlybox(
            ssid=int(ssid.find('Index').text),
            blacklisted_users=[],
            whitelisted_users=[]
        )

        for wifimacblacklist in ssid.findall('.//wifimacblacklist'):
            for item in wifimacblacklist:
                if item.tag.startswith('WifiMacFilterMac'):
                    index = item.tag.replace('WifiMacFilterMac', '')
                    table.blacklisted_users.append(
                        UserDeviceBase(
                            name=ssid.find(f'.//wifihostname{index}').text,
                            mac_address=item.text,
                            ip_address='',
                            interface='',
                            uptime='',
                            active=False,
                            is_local=False,
                        )
                    )

        for wifimacwhitelist in ssid.findall('.//wifimacwhitelist'):
            for item in wifimacwhitelist:
                if item.tag.startswith('WifiMacFilterMac'):
                    index = item.tag.replace('WifiMacFilterMac', '')
                    table.whitelisted_users.append(
                        UserDeviceBase(
                            name=ssid.find(f'.//wifihostname{index}').text,
                            mac_address=item.text,
                            ip_address='',
                            interface='',
                            uptime='',
                            active=False,
                            is_local=False,
                        )
                    )

        return table