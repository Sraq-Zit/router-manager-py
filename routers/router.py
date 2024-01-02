from utils.network import get_gateway_ip


class Router:
    """
    A base class for routers.

    This class provides common functionality and interface for router objects.
    Specific router classes should inherit from this class and implement the
    necessary methods.

    Attributes:
        gateway (str): The gateway IP address of the router.
        username (str): The username for authentication.
        password (str): The password for authentication.

    """

    def __init__(self, username, password):
        """
        Initialize a new Router object.

        Args:
            username (str): The username for authentication.
            password (str): The password for authentication.
        """
        self.gateway = get_gateway_ip()
        self.username = username
        self.password = password

    def login(self) -> bool:
        """
        Login to the router.

        This method should be implemented in derived classes to provide
        router-specific login functionality.

        Returns:
            bool: True if the login was successful, False otherwise.

        Raises:
            NotImplementedError: If the method is not implemented in the derived class.

        """
        raise NotImplementedError("login method must be implemented in derived classes")


    def logout(self):
        """
        Logout from the router.

        This method should be implemented in derived classes to provide
        router-specific logout functionality.

        Returns:
            bool: True if the logout was successful, False otherwise.

        Raises:
            NotImplementedError: If the method is not implemented in the derived class.

        """
        raise NotImplementedError("logout method must be implemented in derived classes")


    def restart_router(self):
        """
        Restart the router.

        This method should be implemented in derived classes to provide
        router-specific restart functionality.

        Raises:
            NotImplementedError: If the method is not implemented in the derived class.

        """
        raise NotImplementedError("restart_router method must be implemented in derived classes")

    def is_supported_router(self):
        """
        Get the router model.

        This method should be implemented in derived classes to provide
        router-specific functionality to retrieve the router model.

        Returns:
            str: The router model.

        Raises:
            NotImplementedError: If the method is not implemented in the derived class.

        """
        # Implement the logic to check if the router is supported
        # Return True or False based on the check
        # You can access the router's properties using self.username, self.password, and self.gateway
        
        raise NotImplementedError("get_router_model method must be implemented in derived classes")

    def get_router_information(self):
        """
        Get the router information.

        This method should be implemented in derived classes to provide
        router-specific functionality to retrieve the router information.

        Returns:
            Information: An instance of the Information class containing the extracted router information.

        Raises:
            NotImplementedError: If the method is not implemented in the derived class.

        """
        raise NotImplementedError("get_router_information method must be implemented in derived classes")
    
    def get_connected_devices(self):
        """
        Get the connected devices.

        This method should be implemented in derived classes to provide
        router-specific functionality to retrieve the connected devices.

        Returns:
            collection: A collection of connected devices.

        Raises:
            NotImplementedError: If the method is not implemented in the derived class.

        """
        raise NotImplementedError("get_connected_devices method must be implemented in derived classes")
    
    def get_mac_filters(self):
        """
        Get the MAC filters.

        This method should be implemented in derived classes to provide
        router-specific functionality to retrieve the MAC filters.

        Returns:
            collection: A collection of MAC filters.

        Raises:
            NotImplementedError: If the method is not implemented in the derived class.

        """
        raise NotImplementedError("get_mac_filters method must be implemented in derived classes")