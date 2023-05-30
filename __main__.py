import sys

from routers.flybox import FlyboxRouter
from utils.network import get_gateway_ip

if __name__ == '__main__':
    # Command-line usage: python main.py username password
    if len(sys.argv) < 3:
        print("Usage: python main.py username password")
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]

    gateway = get_gateway_ip()
    if not gateway:
        print("Gateway not found. Please check your network configuration.")
        sys.exit(1)

    routers = [FlyboxRouter]

    for r_cls in routers:
        router = r_cls(username, password)
        if router.restart_router():
            sys.exit(0)

    print("The current router is not supported/implemented.")
    sys.exit(1)