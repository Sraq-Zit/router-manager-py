import argparse, sys
from routers.flybox import FlyboxRouter
from utils.network import get_gateway_ip

from utils import settings

def main():

    commands = ['info', 'restart', 'devices']

    parser = argparse.ArgumentParser(description='Interact with routers')
    parser.add_argument('username', help='Router username')
    parser.add_argument('password', help='Router password')
    parser.add_argument('action', choices=commands, help='Action to perform: info, restart, devices')
    parser.add_argument('extra', nargs='*', default=[], help='Additional arguments for the devices action')
    parser.add_argument('--as-json', action='store_true', help='Display the information as JSON')

    args = parser.parse_args()

    settings.AS_JSON = args.as_json

    gateway = get_gateway_ip()
    if not gateway:
        print("Gateway not found. Please check your network configuration.")
        return 1

    routers = [FlyboxRouter]

    for r_cls in routers:
        router = r_cls(args.username, args.password)
        if not router.login():
            continue


        if args.action == "info":
            print(router.get_router_information())
        elif args.action == "restart":
            router.restart_router()
        elif args.action.startswith("devices"):
            if args.action == "devices":
                print(router.get_connected_devices().display(not args.extra or args.extra[0] != 'active'))
        
        router.logout()
        return 0

    print("The current router is not supported/implemented.")
    return 1

if __name__ == '__main__':
    sys.exit(main())
