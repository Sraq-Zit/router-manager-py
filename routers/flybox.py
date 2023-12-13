import hashlib
import hmac
import traceback
import xml.etree.ElementTree as ET

import requests

from models.information.flybox import FlyboxInformation
from models.user_device.base import UserDeviceBase, UserDeviceBaseCollection
from routers.router import Router
from utils.xml import merge_xml


class FlyboxRouter(Router):
    """
    A class for performing actions on Flybox router.

    Args:
        username (str): The username for authentication.
        password (str): The password for authentication.
    """

    def __init__(self, username, password):
        super().__init__(username, password)
        self.sess = requests.session()
        self.tokenDictKey = '__requestverificationtoken'


    def _retrieve_token(self):
        """
        Retrieve the authentication token from the router.

        Returns:
            str: The authentication token.
        """
        token_url = f"http://{self.gateway}/api/webserver/token"
        response = self.sess.get(token_url)
        token = ET.fromstring(response.text).find('token').text[32:]
        return token

    def _scram_salted_password(self, salt, iterations):
        """
        Generate the salted password using the SCRAM mechanism.

        Args:
            salt (str): The salt value.
            iterations (int): The number of iterations.

        Returns:
            str: The salted password.
        """
        salted_password = hashlib.pbkdf2_hmac('sha256', self.password.encode(), bytes.fromhex(salt), iterations, dklen=32)
        return salted_password.hex()

    def _scram_client_key(self, salt_password):
        """
        Generate the client key using the SCRAM mechanism.

        Args:
            salt_password (str): The salted password.

        Returns:
            str: The client key.
        """
        salt_password = bytes.fromhex(salt_password)
        client_key = hmac.new("Client Key".encode(), salt_password, hashlib.sha256).hexdigest()
        return client_key

    def _xor_hex_strings(self, ckey_hex, csig_hex):
        """
        Perform XOR operation between two hexadecimal strings.

        Args:
            ckey_hex (str): The first hexadecimal string.
            csig_hex (str): The second hexadecimal string.

        Returns:
            str: The resulting hexadecimal string after XOR operation.
        """
        ckey_bytes = self._bytes_to_words((ckey_hex))
        csig_bytes = self._bytes_to_words((csig_hex))

        result_bytes = list(a ^ b for a, b in zip(ckey_bytes, csig_bytes))
        result_hex = self._words_to_bytes(result_bytes).hex()

        return result_hex

    def _words_to_bytes(self, words):
        """
        Convert a list of words to bytes.

        Args:
            words (list): The input list of words.

        Returns:
            bytes: The converted bytes.
        """
        byte_array = bytearray()
        for word in words:
            # Convert negative word to signed byte representation
            byte_array.extend(word.to_bytes(4, byteorder='big', signed=True))
        return bytes(byte_array)

    def _bytes_to_words(self, byte_array):
        """
        Convert bytes to a list of words.

        Args:
            byte_array (bytes): The input byte array.

        Returns:
            str: The converted list of words.
        """
        word_size = 4
        words = []

        for i in range(0, len(byte_array), word_size):
            word_bytes = byte_array[i:i+word_size]
            word_value = int.from_bytes(word_bytes, byteorder='big', signed=True)
            words.append(word_value)

        return words

    def is_supported_router(self):
        try:
            logout_url = f"http://{self.gateway}/config/global/config.xml"
            response = requests.get(logout_url) 
            return "<title>Flybox</title>" in response.text
        except:
            return False

    def login(self, attempts=3):
        sess = self.sess

        login_state_url = f"http://{self.gateway}/api/user/state-login"
        response = self.sess.get(login_state_url)

        if '<State>0</State>' in response.text:
            return True

        if not self.is_supported_router():
            print("The router is not a Flybox.")
            return False


        token = self._retrieve_token()

        if not token:
            print("Failed to retrieve the token.")
            return False

        sess.headers[self.tokenDictKey] = token
        sess.headers["_responseSource"] = "Browser"

        first_nonce = 'a' * 64

        xml_data = f'<?xml version="1.0" encoding="UTF-8"?><request><username>{self.username}</username><firstnonce>{first_nonce}</firstnonce><mode>1</mode></request>'

        challenge_url = f"http://{self.gateway}/api/user/challenge_login"
        response = sess.post(challenge_url, data=xml_data)
        sess.headers[self.tokenDictKey] = response.headers[self.tokenDictKey]

        try:
            response_tree = ET.fromstring(response.text)

            iterations = int(response_tree.find('iterations').text) if response_tree.find('iterations') is not None else ''
            final_nonce = response_tree.find('servernonce').text if response_tree.find('servernonce') is not None else ''
            salt = response_tree.find('salt').text if response_tree.find('salt') is not None else ''


            auth_msg = f"{first_nonce},{final_nonce},{final_nonce}"

            client_key = self._scram_client_key(self._scram_salted_password(salt, iterations))

            storedKey = hashlib.new('sha256')
            storedKey.update(bytes.fromhex(client_key))
            storedKey = storedKey.hexdigest()

            signature = hmac.new(auth_msg.encode(), bytes.fromhex(storedKey), hashlib.sha256).hexdigest()

            client_proof = self._xor_hex_strings(bytes.fromhex(client_key), bytes.fromhex(signature))


            xml_data = f'<?xml version: "1.0" encoding="UTF-8"?><request><clientproof>{client_proof}</clientproof><finalnonce>{final_nonce}</finalnonce></request>'
            authentication_url = f"http://{self.gateway}/api/user/authentication_login"
            response = sess.post(authentication_url, data=xml_data)

            if '<serversignature>' in response.text:
                return True
            else:
                print('Could not login', response.text)
        except Exception as ex:
            if attempts > 0:
                return self.login(attempts - 1)
            traceback.print_exc()
            print('Failed to log in. This is usually caused by multiple logins. Please try again later.')
            return False

    def logout(self):
        if self.login():
            self.sess.headers[self.tokenDictKey] = self._retrieve_token()
            xml_data = f'<?xml version: "1.0" encoding="UTF-8"?><request><Logout>1</Logout></request>'
            control_url = f"http://{self.gateway}/api/user/logout"
            response = self.sess.post(control_url, data=xml_data)
            success = '<response>OK</response>' not in response.text
            if success: print('Failed to logout', response.text)
            return success


    def get_router_information(self):
        info_url = f"http://{self.gateway}/api/device/information"
        signal_url = f"http://{self.gateway}/api/device/signal"

        xml = merge_xml(
            self.sess.get(info_url).text,
            self.sess.get(signal_url).text,
        )

        return FlyboxInformation.from_xml_string(xml)

    def restart_router(self):
        if not self.gateway:
            print("Gateway not found. Please check your network configuration.")
            return False

        if self.login():
            self.sess.headers[self.tokenDictKey] = self._retrieve_token()

            # Restarting ..
            xml_data = f'<?xml version: "1.0" encoding="UTF-8"?><request><Control>1</Control></request>'
            control_url = f"http://{self.gateway}/api/device/control"
            response = self.sess.post(control_url, data=xml_data)

            success = '<response>OK</response>' in response.text

            if success:
                print('Restarting router 🔃')
            else:
                print('Something went wrong', response.text)

            return success

        return False

    def get_connected_devices(self, include_disconnected=False):
        if not self.gateway:
            print("Gateway not found. Please check your network configuration.")
            return False

        if self.login():
            control_url = f"http://{self.gateway}/api/lan/HostInfo"
            response = self.sess.get(control_url)

            root = ET.fromstring(response.text)
            
            devices = [
                UserDeviceBase(
                    node.find('ActualName').text,
                    node.find('IpAddress').text,
                    node.find('MacAddress').text,
                    node.find('InterfaceType').text,
                    24 * 3600 - int(node.find('LeaseTime').text),
                    node.find('Active').text == '1'
                ) for node in root.findall('Hosts/Host')
            ]


            return UserDeviceBaseCollection(devices)
