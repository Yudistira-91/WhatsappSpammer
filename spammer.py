from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time

def createDriverInstance():
    options = webdriver.ChromeOptions()
    options.add_argument('log-level=3')
    #options.add_argument('--headless')
    args = ["hide_console", ]
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--user-data-dir=C:\\Users\\Barak\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1")
    driver = webdriver.Chrome(options=options, executable_path=r'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe', service_args=args)
    driver.get("https://web.whatsapp.com/")
    return driver


def find_user(username, driver):
    for i in range(5):
        try:
            print('\nStarting program...')
            user = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, f'//*[@title="{username}"]')))
            print('Program is running!\n')
            user.click()
            time.sleep(1)
            user.click()
            return True
        except:
            continue
    return False

def run(username="Dor", text_file_name="zombie", time_to_wait="10"):
    driver = createDriverInstance()
    is_user_found = find_user(username, driver)

    while not is_user_found:
        driver.maximize_window()
        print('friend not found, please enter your friend name again...\n')
        is_user_found = find_user(input('enter friend name: '), driver)

    while is_user_found:
        try:
            chat = WebDriverWait(driver, 50).until(
                EC.presence_of_element_located((By.CLASS_NAME, '_13mgZ')))
            chat.click()
            text_file = open(f"../textFiles/{text_file_name}.txt", "r", encoding="utf8") 
            for line in text_file:
                print(f'message: {line}\nsent at: {datetime.datetime.now().time()}\n')
                chat.send_keys(line)
                time.sleep(int(time_to_wait))
            text_file.close()
        except:
            is_user_found = find_user(username, driver)
            if not is_user_found:
                print('error user not found, stopping program...')
                time.sleep(5)
                break
            continue

if __name__ == '__main__':
    run()
