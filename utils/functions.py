import json
from utils import settings

def handle_message(key, code, details=''):
    message = code[1] + ' ' + details
    if settings.AS_JSON:
        message = json.dumps({key: code[0], 'message': message})
    print(message)

def handle_info(code, details=''):
    handle_message('info', code, details)

def handle_error(code, details = ''):
    handle_message('error', code, details)