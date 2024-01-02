import argparse, sys
from routers.flybox import FlyboxRouter
from utils.consts import GATEWAY_ERROR, INCOMPATIBLE, ROUTER_NOT_SUPPORTED
from utils.functions import handle_error
from utils.network import get_gateway_ip

from utils import settings

def main():

    commands = ['info', 'restart', 'devices', 'macfiltering']

    parser = argparse.ArgumentParser(description='Interact with routers')
    parser.add_argument('username', help='Router username')
    parser.add_argument('password', help='Router password')
    parser.add_argument('action', choices=commands, help='Action to perform: info, restart, devices')
    parser.add_argument('extra', nargs='*', default=[], help='Additional arguments for the devices action')
    parser.add_argument('-j', '--as-json', action='store_true', help='Print output as JSON')

    args = parser.parse_args()

    settings.AS_JSON = args.as_json

    gateway = get_gateway_ip()
    if not gateway:
        handle_error(GATEWAY_ERROR)
        return 1

    routers = [FlyboxRouter]

    for r_cls in routers:
        router = r_cls(args.username, args.password)
        results, response_text = router.login()

        if results != True:
            if results == INCOMPATIBLE: continue
            handle_error(results)
            return 1

        if args.action == "info":
            print(router.get_router_information())
        elif args.action == "restart":
            router.restart_router()
        elif args.action == 'macfiltering':
            print(router.get_mac_filters().display())
        elif args.action.startswith("devices"):
            if args.action == "devices":
                print(router.get_connected_devices().display())
        
        router.logout()
        return 0

    handle_error(ROUTER_NOT_SUPPORTED)
    return 1

if __name__ == '__main__':
    sys.exit(main())
