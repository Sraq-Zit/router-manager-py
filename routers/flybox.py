import hashlib
import hmac
import sys
import traceback
import xml.etree.ElementTree as ET

import requests

from routers.router import Router


class FlyboxRouter(Router):
    """
    A class for restarting a router by performing authentication using the SCRAM mechanism.

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

    def _authenticate_router(self):
        """
        Authenticate and restart the router.

        Returns:
            int: The exit code (0 for success, 1 for failure).
        """
        sess = self.sess

        config_url = f"http://{self.gateway}/config/global/config.xml"
        response = sess.get(config_url)

        if "<title>Flybox</title>" not in response.text:
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

            # print(sess.get(f"http://{self.gateway}/html/content.html").text)

            sess.headers[self.tokenDictKey] = self._retrieve_token()

            # Restarting ..
            xml_data = f'<?xml version: "1.0" encoding="UTF-8"?><request><Control>1</Control></request>'
            control_url = f"http://{self.gateway}/api/device/control"
            response = sess.post(control_url, data=xml_data)

            if '<response>OK</response>' in response.text:
                print('Restarting router 🔃')
            else:
                print('Something went wrong', response.text)
                return False

            return True
        except Exception as ex:
            traceback.print_stack()
            print('Failed to log in. This is usually caused by multiple logins. Please try again later.')
            return False


    def is_available(self):
        try:
            config_url = f"http://{self.gateway}/config/global/config.xml"
            response = requests.get(config_url) 
            return "<title>Flybox</title>" in response.text
        except:
            return False


    def restart_router(self):
        """
        Restart the router by performing authentication.

        Returns:
            int: The exit code (0 for success, 1 for failure).
        """

        if not self.gateway:
            print("Gateway not found. Please check your network configuration.")
            return False

        return self._authenticate_router()
