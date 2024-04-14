from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def main():
    driver = webdriver.Chrome()

    driver.get("https://npg-team.itch.io/product-owner-simulator")
    driver.fullscreen_window()
    
    driver.implicitly_wait(30)

    load_iframe_btn = driver.find_element(by=By.CLASS_NAME, value="load_iframe_btn")
    load_iframe_btn.click()

    fullscreen_btn = driver.find_element(by=By.CLASS_NAME, value='fullscreen_btn')
    fullscreen_btn.click()

    # time.sleep(5)

    driver.quit()

if __name__ == '__main__':
    main()
