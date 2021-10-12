import json
import logging
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

class SeleniumOperate:
    logger = logging.getLogger(__name__)

    @staticmethod
    def create_chrome(client_ip=None, proxy=None, user_agent=None, display_image=False, headless=None):

        try:
            chrome_options: Options = webdriver.ChromeOptions()
            prefs = {"profile.managed_default_content_settings.notifications": 2,
                     "profile.managed_default_content_settings.images": 2,
                     "intl.accept_languages": "en-us,us",
                     "webrtc.ip_handling_policy": "disable_non_proxied_udp", "webrtc.multiple_routes_enabled": False,
                     "webrtc.nonproxied_udp_enabled": False}

            if display_image:
                prefs["profile.managed_default_content_settings.images"] = 0

            #desired_capabilities = {"browserstack.timezone": "Volgograd"}
            chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_experimental_option("detach", True)
            chrome_options.add_experimental_option("prefs", prefs)
            chrome_options.add_argument("--disable-default-apps")
            chrome_options.add_argument("--disable-system-timezone-automatic-detection")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--homepage=chrome://version/")
            chrome_options.add_argument("--–window-size=800,600")
            chrome_options.add_argument('--lang=es-US')


            if proxy is not None and proxy.strip() != "":
                chrome_options.add_argument("--proxy-server=" + proxy)
            if user_agent is not None and user_agent.strip() != "":
                chrome_options.add_argument("--user-agent=" + user_agent)
            if headless is not None and headless.strip() != "":
                chrome_options.add_argument("--headless")
            if client_ip is not None and client_ip.strip() != "":
                desired_capabilities = {'browserName': 'chrome',
                                        'version': '',
                                        'platform': 'ANY',
                                        'javascriptEnabled': True
                                        # 'webdriver.chrome.driver': 'D:\\PycharmProjects\\selenium_server\\chromedriver.exe'
                                        }
                driver = webdriver.Remote(command_executor="http://{0}:4444/wd/hub".format(client_ip),
                                          options=chrome_options, desired_capabilities=desired_capabilities)
            else:
                driver = webdriver.Chrome(chrome_options=chrome_options)
            if driver is not None:
                driver.set_page_load_timeout(60)
            driver.maximize_window()
            return driver
        except Exception as ex:
            print(ex)
            return None

    @staticmethod
    def open_url(driver: webdriver, url: str, logger: logging):
        try:
            logger.info("正在打开Url:{0}".format(url))
            driver.get(url)
            logger.info("打开Url完成")
        except Exception as ex:
            logger.info("打开Url失败" + str(ex))

    @staticmethod
    def get_cookies(driver: webdriver, domain: str):
        try:
            cookies = []
            for cookie in driver.get_cookies():
                if cookie.__contains__("domain") and cookie["domain"].find(domain) >= 0:
                    cookies.append({"name": cookie["name"], "value": cookie["value"], "domain": cookie["domain"]})
            return cookies
        except:
            return None

    @staticmethod
    def set_cookies(driver: webdriver, cookie_str: str, domain: str):
        try:
            logging.info("正在转换cookie")
            cookies = json.loads(cookie_str)
            if len(cookies) > 0:
                #logging.info("需要设置Cookie:{0}".format(cookies))
                logging.info("开始设置cookie")
                # driver.delete_all_cookies()
                for cookie in cookies:
                    if cookie.__contains__("domain") and cookie["domain"].find(domain) >= 0:
                        cookie["expiry"] = 1713500918
                        cookie["httpOnly"] = True
                        cookie["secure"] = True
                        driver.add_cookie(cookie)
                # logging.info("当前页面Cookie:{0}".format(driver.get_cookies()))
                logging.info("刷新页面")
                driver.refresh()
                # logging.info("当前页面Cookie:{0}".format(driver.get_cookies()))
        except:
            logging.info("程序异常")

    # @staticmethod
    #  find_element_and_send_keys(css: str,value: str,desc: str=None):

    @staticmethod
    def send_keys(name, element, value):
        try:
            logging.info("输入{0}".format(name))
            element.clear()
            sleep(random.uniform(0, 2))
            element.send_keys(value)
            sleep(random.uniform(2, 4))
        except:
            pass

    @staticmethod
    def click(name, element):
        try:
            logging.info("点击{0}".format(name))
            element.click()
            sleep(random.uniform(3, 5))
        except:
            pass

    @staticmethod
    def select(name, element, value):
        try:
            logging.info("选择{0}".format(name))
            Select(element).select_by_value(value)
            sleep(random.uniform(3, 5))
        except:
            pass
