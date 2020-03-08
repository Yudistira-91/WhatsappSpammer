from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

from spammer import create_driver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import requests
import datetime
import time


def request_song_info(song_title):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': f'Bearer wp0gswBrqZQQ2__BOF6EIllAI8PcVb_g-ezd-J0NG8ogekKeua_0AdfhuddyU73b'}
    search_url = base_url + '/search'
    data = {'q': song_title}
    response = requests.get(search_url, data=data, headers=headers)
    return response


def scrape_song_url(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    return html.find('div', class_='lyrics').get_text()


def send_text(lyrics, driver):
    chat = driver.find_elements_by_css_selector('[contenteditable="true"]')[-1]
    chat.click()
    for line in lyrics.split('\n'):
        driver.execute_script('arguments[0].appendChild(document.createTextNode(arguments[1]))', chat, line + '\n')
    chat.send_keys('u')
    chat.send_keys(Keys.BACKSPACE)
    send_button = driver.find_elements_by_css_selector('button')[-1]
    send_button.click()


def genius_search_lyrics(genius_song_title, driver):
    response = request_song_info(genius_song_title)
    json = response.json()
    remote_song_info = None
    if len(json['response']['hits']) == 0:
        send_text(f'The song "{genius_song_title}" not found.', driver)
        return False

    text = f'Song title: "{genius_song_title}"\nPlease choose an artist from this list: \n'

    for i, hit in enumerate(json['response']['hits']):
        text += f"{i + 1}. {hit['result']['full_title']}\n"

    text += "\n\nWrite 'cancel' to cancel."
    send_text(text, driver)

    while True:
        time.sleep(0.2)
        last_message = driver.find_elements_by_class_name('_F7Vk')[-1].text
        if last_message.isnumeric() and int(last_message) < len(text):
            remote_song_info = json['response']['hits'][int(last_message) - 1]
            break
        elif last_message.lower() == 'cancel':
            send_text('Search canceled.', driver)
            break

    if remote_song_info:
        song_url = remote_song_info['result']['url']
        send_text(scrape_song_url(song_url), driver)
        return True
    return False


def get_latest_message(driver):
    messages = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'X7YrQ')))
    up_to_date_messages = []
    for message in messages:
        try:
            text = message.find_element_by_class_name('_0LqQ').text
            if text.strip().replace(':', '').isnumeric():
                up_to_date_messages.append(message)
        except (StaleElementReferenceException, NoSuchElementException):
            pass
    return sorted(up_to_date_messages, key=lambda msg: msg.find_element_by_class_name('_0LqQ').text, reverse=True)[0]


def run():
    driver = create_driver()
    search_text = 'מילים לשיר '

    while True:
        time.sleep(1)
        print(f'program running: {datetime.datetime.now().time()}')
        try:
            latest_message = get_latest_message(driver)
            message_text = latest_message.find_elements_by_class_name('_19RFN')[-1].text
            if len(message_text) >= 10 and message_text.startswith(search_text):
                genius_song_title = message_text.replace(search_text, '')
                latest_message.click()
                genius_search_lyrics(genius_song_title, driver)
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    run()
