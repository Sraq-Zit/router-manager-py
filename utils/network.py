import subprocess


def get_gateway_ip():
        """
        Get the gateway IP address.

        Returns:
            str: The gateway IP address.
        """
        try:
            gateway = subprocess.check_output(["ip", "route", "show", "default"]).split()[2].decode('utf-8')
            return gateway
        except subprocess.CalledProcessError:
            return None