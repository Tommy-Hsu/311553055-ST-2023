from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)


def main():

    # 打開交大
    browser = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    browser.get("https://www.nycu.edu.tw/")

    # 放大視窗
    browser.maximize_window()

    # 找到新聞頁面
    news = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'elementor-item') and (By.LINK_TEXT, '新聞')), message="get it!!!")
    news.click()

    # 打開第一份新聞
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    tab_contents = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'eael-tabs-content')))
    # tab_contents = browser.find_element(By.CLASS_NAME, 'eael-tabs-content')
    first = tab_contents.find_element(By.CLASS_NAME, 'su-posts.su-posts-list-loop')
    target = first.find_elements(By.TAG_NAME, 'a')
    title = target[0].get_attribute("title")
    print(title)
    target[0].click()
    hold_on = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'article')))
    para = browser.find_elements(By.XPATH, "//article/div/p | //article/div/figure/figcaption")
    for i in range(len(para)):
        print(para[i].text)

    # open a new tab and switch to it
    browser.switch_to.new_window('tab')
    browser.get("https://www.google.com")

    # input your student number and submit
    search = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'gLFyf')))
    search.send_keys('311553055')
    search.send_keys(Keys.RETURN)

    # print the title of second result
    hold_on = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'rso') and (By.CLASS_NAME, 'v7W49e')), message='nothing')
    #result = browser.find_elements(By.XPATH, "//h3[contains(@class, 'LC20lb MBeuO DKV0Md')]")
    result = browser.find_elements(By.TAG_NAME, 'h3')
    ele = result[0].text
    for i in range(len(result)):
        if (result[i].text != ele) and (result[i].get_attribute("class") != "GmE3X"):
            print(result[i].text)
            break
    

    # 檢查
    time.sleep(5)
    browser.quit()


if __name__ == "__main__":
    main()