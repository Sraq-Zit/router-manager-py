import json
import subprocess

from utils import settings
from utils.consts import GATEWAY_ERROR


def get_gateway_ip():
    """
    Get the gateway IP address.

    Returns:
        str: The gateway IP address.
    """
    try:
        stdout = subprocess.check_output(["ip", "route", "show", "default"])
        if not stdout:
            return None
        return stdout.split()[2].decode('utf-8')
    except subprocess.CalledProcessError:
        return None

