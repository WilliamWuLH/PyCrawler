from selenium import webdriver
from selenium.webdriver.common.keys import Keys

if __name__ == "__main__":
    browser = webdriver.Chrome('D:\ChromeDriver\chromedriver.exe')
    browser.get('https://www.baidu.com/')
    # //*[@id="kw"]
    elem = browser.find_element_by_xpath('//*[@id="kw"]')
    elem.send_keys('吴林瀚')
    # elem.send_keys(Keys.RETURN)
    browser.find_element_by_xpath('//*[@id="su"]').click()