from spammer import createDriverInstance, find_user
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import requests
import datetime
import time

def request_song_info(song_title):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + 'API KEY'}
    search_url = base_url + '/search'
    data = {'q': song_title}
    response = requests.get(search_url, data=data, headers=headers)
    return response

def scrap_song_url(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', class_='lyrics').get_text()

    return lyrics

def send_text(lyrics, driver):
    chat = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, '_13mgZ')))
    chat.click()
    for line in lyrics.split('\n'):
        chat.send_keys(line)
        ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
    send_button = driver.find_elements_by_class_name('_3M-N-')[0]
    send_button.click()

def geniues_search_lyrics(geniues_song_title, driver):
    response = request_song_info(geniues_song_title)
    json = response.json()
    remote_song_info = None
    if len(json['response']['hits']) == 0:
        send_text(f'The song "{geniues_song_title}" not found.', driver)
        return False

    artists = f'Song title: "{geniues_song_title}"\nPlease choose a artist from this list: \n'

    for ind, hit in enumerate(json['response']['hits']):
        artists = f"{artists}\n{ind+1}. {hit['result']['primary_artist']['name']}"

    artists = artists + "\n\nWrite 'cancel' to cancel."
    send_text(artists, driver)

    while True:
        last_message = driver.find_elements_by_class_name('_F7Vk')[-1].text
        if last_message.isnumeric() and int(last_message) < len(artists):
            remote_song_info = json['response']['hits'][int(last_message) - 1]
            break
        elif last_message.lower() == 'cancel':
            send_text('Search canceled.', driver)
            break

    if remote_song_info:
        song_url = remote_song_info['result']['url']
        send_text(scrap_song_url(song_url), driver)
        return True
    return False


def run():
    driver = createDriverInstance()
    username = 'Dor'
    find_user(username, driver)

    while True:
        time.sleep(1)
        print(f'program running: {datetime.datetime.now().time()}')
        try:
            messages = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, '_19RFN')))
            for message in messages:
                if len(message.text) >= 10 and message.text[0:11] == 'מילים לשיר ':
                    geniues_song_title = message.text.replace('מילים לשיר ', '')
                    message.click()
                    geniues_search_lyrics(geniues_song_title, driver)
        except:
            break

if __name__ == '__main__':
    run()
