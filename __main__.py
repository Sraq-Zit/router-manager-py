import sys

from routers.flybox import FlyboxRouter
from utils.network import get_gateway_ip


def main():
    if len(sys.argv) != 4:
        print("Usage: python main.py {info|restart} username password")
        return

    action = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    gateway = get_gateway_ip()
    if not gateway:
        print("Gateway not found. Please check your network configuration.")
        sys.exit(1)

    routers = [FlyboxRouter]

    for r_cls in routers:
        router = r_cls(username, password)
        if not router.login():
            continue

        if action == "info":
            print(router.get_router_information())
        elif action == "restart":
            router.restart_router()
        else:
            print("Invalid action. Supported actions are 'info' and 'restart'.")
        
        return router.logout()

    print("The current router is not supported/implemented.")

if __name__ == '__main__':
    main()