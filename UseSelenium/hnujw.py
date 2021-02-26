from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import requests
import time
import logging
import re

class HnuJW(object):

    def __init__(self):
        self.driver = webdriver.Chrome('D:\ChromeDriver\chromedriver.exe')
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.actionchains = ActionChains(self.driver)
        self.url = 'http://hdjw.hnu.edu.cn/'
    
    def login(self, username, password):
        while True:
            self.driver.get(self.url)
            time.sleep(1)

            # 输入用户名
            self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[2]/form/div[2]/div/div/input').send_keys(username)
            # 输入密码
            self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[2]/form/div[3]/div/div/input').send_keys(password)
            # 点击登录
            self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[2]/form/div[5]/div/button/span').click()
            time.sleep(3)
            # 学生门户
            xsmh = self.driver.find_element_by_class_name('el-submenu__title')
            self.actionchains.move_to_element(xsmh).click(xsmh).perform()
            time.sleep(2)

            # 验证是否登录成功
            try :
                information = self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/div[1]/div/div[1]/form/div[2]/div/div[1]/div[1]/div[1]/div/div[2]/div[1]/p')
                id_num = information.text.split(' ')[-1]
                # id_num = re.match(r'(\d){12}', information.text) 
                print(id_num)
                if id_num == username:
                    break
            except NoSuchElementException:
                logging.info(NoSuchElementException)            

    def academicProgressChart(self):
        # 培养方案
        pyfa = self.driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/div/div/div[1]/div/div[2]/ul/div/li[6]/div/span')
        self.actionchains.move_to_element(pyfa).click(pyfa).perform()
        time.sleep(2)

        # 学业进展表
        self.driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/div/div/div[1]/div/div[2]/ul/div/li[6]/ul/div/li[3]/span[2]').click()
        time.sleep(3)
        

if __name__ == "__main__":
    username = '201707020322'
    password = 'WLH199990301'
    stu = HnuJW()
    stu.login(username, password)
    stu.academicProgressChart()