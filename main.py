import random
from SeleniumTest import Test
from Tools import Tools

if __name__ == '__main__':
    ua = random.choice(Tools.read_yaml('settings.yaml')['USER_AGENT'])  # 获取配置文件ua
    test = Test(client_ip='', proxy='', user_agent=ua, headless=None)
    test.baidu()