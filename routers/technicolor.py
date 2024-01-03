
import re
import traceback
import requests
from models.information.technicolor import TechnicolorInformation
from routers.router import Router
from utils import settings
from utils.consts import INCOMPATIBLE, SOMETHING_WRONG

from bs4 import BeautifulSoup as bs


class TechnicolorRouter(Router):
        
    def __init__(self, username, password):
        super().__init__(username, password)
        self.sess = requests.session()

    def is_supported_router(self):
        login_state_url = f"http://{self.gateway}/Wizard/ge_login.cgi"
        html = self.sess.get(login_state_url).text
        return '<p id="productName" class="product"> Technicolor' in html
        
    
    def login(self, attempts=3):

        login_state_url = f"http://{self.gateway}/Wizard/ge_login.cgi"

        if not self.is_supported_router():
            if not settings.AS_JSON:
                print("The router is not a Flybox.")
            return INCOMPATIBLE, ''

        try:
            response = self.sess.post(login_state_url, {
                'user': self.username,
                'password': self.password,
                'isSubmit': '1',
            })

            if 'Set-Cookie' in response.headers:
                return True, response
            
            return False, response

        except Exception as ex:
            if attempts > 0:
                return self.login(attempts - 1)
            if not settings.AS_JSON:
                traceback.print_exc()
                print(
                    'Failed to log in. This is usually caused by multiple logins. Please try again later.'
                )
            return SOMETHING_WRONG, ''

    def logout(self):
        self.sess.cookies.clear()

    def get_router_information(self):
        information_url = f"http://{self.gateway}/Wizard/ge_gateway.cgi?be=0&l0=1&l1=0&pageAct=info"
        response = self.sess.get(information_url)
        doc = bs(response.text, 'html.parser')
        return TechnicolorInformation(
            device_name=doc.select(id="td[colspan='3']")[0].text.strip(),
            serial_number=doc.select(id="td[colspan='3']")[1].text.strip(),
            software_version=doc.select(id="td[colspan='3']")[2].text.strip(),
        )

    
