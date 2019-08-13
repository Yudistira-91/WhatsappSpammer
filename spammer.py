from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
import time 

driver = webdriver.Chrome(executable_path=r'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe') 
 
driver.get("https://web.whatsapp.com/")
time.sleep(8) #delay time for connecting your whatsapp at web
driver.get("https://web.whatsapp.com/")

friend_name = "Dor"

while True:
    try:
        driver.find_element_by_xpath(f'//*[@title="{friend_name}"]').click()
        break
    except:
        continue

chat = driver.find_element_by_class_name('_3u328')
chat.click()
for i in range(10):
    bird_is_the_word  = open("textToSend.txt", "r") 
    for line in bird_is_the_word:
        chat.send_keys(line)
    bird_is_the_word.close()
