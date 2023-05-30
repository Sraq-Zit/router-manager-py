from utils.network import get_gateway_ip


class Router:
    """
    A base class for routers.

    This class provides common functionality and interface for router objects.
    Specific router classes should inherit from this class and implement the
    necessary methods.

    Attributes:
        username (str): The username for authentication.
        password (str): The password for authentication.
        gateway (str): The gateway IP address of the router.

    """

    def __init__(self, username, password):
        """
        Initialize a new Router object.

        Args:
            username (str): The username for authentication.
            password (str): The password for authentication.
            gateway (str): The gateway IP address of the router.

        """
        self.gateway = get_gateway_ip()
        self.username = username
        self.password = password

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

    def get_router_model(self):
        """
        Get the router model.

        This method should be implemented in derived classes to provide
        router-specific functionality to retrieve the router model.

        Returns:
            str: The router model.

        Raises:
            NotImplementedError: If the method is not implemented in the derived class.

        """
        raise NotImplementedError("get_router_model method must be implemented in derived classes")
