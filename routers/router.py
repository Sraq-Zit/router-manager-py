from utils.network import get_gateway_ip


class Router:
    def __init__(self, username, password):
        self.gateway = get_gateway_ip()
        self.username = username
        self.password = password

    def restart_router(self):
        raise NotImplementedError("restart_router method must be implemented in derived classes")
