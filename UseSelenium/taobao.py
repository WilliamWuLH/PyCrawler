from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver import ActionChains
from retrying import retry
import logging
import time
import cv2
import pyautogui
pyautogui.PAUSE = 0.5

# logging
logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
logger = logging.getLogger(__name__)

class taobao(object):
    
    def __init__(self):
        option = webdriver.ChromeOptions()
        # 防止打印一些无用的日志
        option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        self.browser = webdriver.Chrome('D:\ChromeDriver\chromedriver.exe',chrome_options=option)
        self.browser.maximize_window()
        self.browser.implicitly_wait(5)
        self.domain = 'https://www.taobao.com'
        self.action_chains = ActionChains(self.browser)

    def login(self, username, password):
        while True:
            self.browser.get(self.domain)
            time.sleep(1)

            # 找到登录的链接，点击
            self.browser.find_element_by_xpath('//*[@id="J_SiteNavLogin"]/div[1]/div[1]/a[1]').click()
            # 输入用户名
            self.browser.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys(username)
            # 输入密码
            self.browser.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys(password)
            time.sleep(3)

            try:
                # 出现验证码，滑动验证
                slider = self.browser.find_element_by_xpath("//span[contains(@class, 'btn_slide')]")
                if slider.is_displayed():
                    print('slider display')
                    # 拖拽滑块
                    self.action_chains.drag_and_drop_by_offset(slider, 258, 0).perform()
                    time.sleep(0.5)
                    # 释放滑块，相当于点击拖拽之后的释放鼠标
                    self.action_chains.release().perform()
            except (NoSuchElementException, WebDriverException):
                logger.info('未出现登录验证码')

            # 登录按钮
            # self.browser.find_element_by_xpath('//*[@id="login-form"]/div[4]/button').click()
            img = cv2.imread(r'./taobaologin.jpg')
            coords = pyautogui.locateOnScreen(img)
            x, y = pyautogui.center(coords)
            pyautogui.leftClick(x, y)

            # 验证是否登陆成功
            nickname = self.get_nickname()
            if nickname:
                logger.info('登陆成功，昵称为：' + nickname)
                break
            logger.debug('登录出错，5s 后继续登录')
            time.sleep(5)
    
    def get_nickname(self):
        self.browser.get(self.domain)
        time.sleep(0.5)
        try:
            return self.browser.find_element_by_class_name('site-nav-user').text
        except NoSuchElementException:
            return ''

if __name__ == '__main__':
    username = 't_1500616547752_0101'
    password = 'WLH199990301'
    tb = taobao()
    tb.login(username, password)


    
