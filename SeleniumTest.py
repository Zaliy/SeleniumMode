import json
import logging
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from SeleniumOperate import SeleniumOperate
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

class Test:
    def __init__(self, client_ip: str, proxy: str, user_agent:str, headless):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S')
        self.logger = logging.getLogger('Main')
        self.client_ip = client_ip
        self.proxy = proxy
        self.user_agent = user_agent
        self.driver = None
        self.headless = headless
        self.wait = None

    def create_chrome(self):
        self.driver = SeleniumOperate.create_chrome(client_ip=self.client_ip, proxy=self.proxy,
                                                    user_agent=self.user_agent, headless=self.headless)
        if self.driver is not None:
            self.logger.info("浏览器启动成功")
            self.wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1)
            return True
        else:
            self.logger.info(("浏览器启动失败"))
            return False

    def baidu(self):
        if self.driver is None:
            self.create_chrome()
        if self.driver is not None:
            SeleniumOperate.open_url(self.driver, "https://www.baidu.com", self.logger)

    def get_cookies(self):
        cookies = SeleniumOperate.get_cookies(self.driver, "facebook.com")
        if cookies is not None:
            return json.dumps(cookies, separators=(',', ':'))
        return None

    def find_visibility_element(self, css):
        try:
            return self.wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, css)))
        except:
            return None

    def find_visibility_elements(self, css):
        try:
            return self.wait.until(ec.visibility_of_all_elements_located((By.CSS_SELECTOR, css)))
        except:
            return None

    def find_exists_element(self, css):
        try:
            return self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, css)))
        except:
            return None

    def find_exists_elements(self, css):
        try:
            return self.wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, css)))
        except:
            return None

    def close(self):
        try:
            self.driver.quit()
        except:
            pass