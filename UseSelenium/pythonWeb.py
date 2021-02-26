from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys

if __name__ == "__main__":
    driver = Chrome('D:\ChromeDriver\chromedriver.exe')
    driver.get('https://www.python.org')
    assert 'Python' in driver.title
    
    elem = driver.find_element_by_name('q')
    elem.send_keys('pypi')
    elem.send_keys(Keys.RETURN)
    print(driver.page_source)