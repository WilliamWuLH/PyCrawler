from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from aip import AipOcr
from matplotlib import pyplot as plt
import requests
import random
import logging
import time
import os


class HnuYqfk(object):

    def __init__(self):

        self.driver = webdriver.Chrome('D:\ChromeDriver\chromedriver.exe')
        self.driver.implicitly_wait(5)
        # self.driver.maximize_window()
        self.actionchains = ActionChains(self.driver)

        self.url = 'https://fangkong.hnu.edu.cn/app/#/login'
        self.img_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'yzm_img.jpg')

        # OCR
        self.AppID = '23732462'
        self.API_Key = 'ucRRZMndUiDsIvY5uTDFvEGr'
        self.Secret_Key = 'q4zSl6KhtR0tMjsPaDlFG2MhhYlyb8vY'
    
    def login(self, username, password):

        while True:

            self.driver.get(self.url)
            time.sleep(1)

            # username
            self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[1]/input').send_keys(username)
            # password
            self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/input').send_keys(password)
            time.sleep(1)

            # 验证码图片
            while True:
                if self.get_yzm_img():
                    break

            # OCR
            words = ''
            while len(words) < 4:
                words = self.yzm_img_OCR()
            
            self.driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[3]/div/input').send_keys(words)
            time.sleep(1)

            self.driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/button').click()
            self.driver.implicitly_wait(5)

            try:
                mrdk = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[1]/div/div/div/div[1]/span')
                if mrdk.is_displayed():
                    break
            
            except Exception as e:
                logging.info(e)
    
    def get_yzm_img(self):

        self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[3]/div/input').click()
        time.sleep(1)

        img = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[3]/img')
        img_url = img.get_attribute('src')
        r = requests.get(url=img_url)

        if r.status_code == 200:
            with open(self.img_path, 'wb') as f:
                f.write(r.content)
            return True

        return False
    
    def yzm_img_OCR(self):

        client = AipOcr(self.AppID, self.API_Key, self.Secret_Key)

        with open(self.img_path, 'rb') as f:
            res = client.numbers(f.read())
            words = res['words_result'][0]['words']
            print(words)

        return words
    
    def clock_in(self, loc, t_am, t_pm):

        t_am = '36.5' if t_am < 36 or t_am > 37 else str(t_am)
        t_pm = '36.5' if t_pm < 36 or t_pm > 37 else str(t_pm)

        print(loc)
        print(t_am)
        print(t_pm)

        self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[1]/div/div/div/div[1]').click()
        time.sleep(1)

        self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div[2]/div[2]/i').click()
        time.sleep(0.5)
        
        for i in range(2, 19):
            self.driver.find_element_by_xpath('//*[@id="app"]/div/div[5]/div/div[2]/div[1]/ul/li[{}]'.format(i)).click()

        for i in range(2, 4):
            self.driver.find_element_by_xpath('//*[@id="app"]/div/div[5]/div/div[2]/div[3]/ul/li[{}]'.format(i)).click()

        self.driver.find_element_by_xpath('//*[@id="app"]/div/div[5]/div/div[1]/button[2]').click()

        self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div[2]/div[3]/div[2]/div/input').send_keys(loc)

        self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div[3]/div/div[2]/div[2]/input').send_keys(t_am)

        self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/input').send_keys(t_pm)

        self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div[1]/div/div/div/div[2]/button').click()

    def check(self):

        self.driver.implicitly_wait(5)
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[1]/div/div/div/div[1]').click()
        time.sleep(1)

        today = self.driver.find_element(By.CLASS_NAME, "wh_item_date.wh_isToday.mark-state-0")

        if today.is_displayed():
            today.click()
            print('已打卡')
            return False
        
        return True

if __name__ == "__main__":

    username = '201707020322'
    password = 'Wlh199990301'

    location = '湖南大学德智园学生公寓 10 栋'

    temperature_am = round(random.uniform(36, 37), 1)
    temperature_pm = round(random.uniform(36, 37), 1)

    stu = HnuYqfk()
    stu.login(username, password)

    while stu.check():
        stu.clock_in(location, temperature_am, temperature_pm)