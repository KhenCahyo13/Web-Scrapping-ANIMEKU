from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from slugify import slugify
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'helpers')))

import generate_random_id

load_dotenv()
base_url = os.getenv('ANIMEKU_BASE_URL')
external_storage_path = os.getenv('EXTERNAL_STORAGE_PATH')
driver = webdriver.Chrome();

def main() :
    iterate_anime()

def create_url_list ():
    urls = []

    for i in range (1, 3):
        urls.append(f"{base_url}nonton-anime/?page={i}")

    return urls

def scrap_anime_list():
    urls = create_url_list()
    anime_elements = []

    for url in urls:
        driver.get(url)
        
        anime_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'listupd'))
        )
        anime_html = anime_element.get_attribute('outerHTML')
        soup = BeautifulSoup(anime_html, 'lxml')
        anime_elements.extend(soup.find_all('article'))

    return anime_elements

def iterate_anime():
    anime_list = scrap_anime_list()
    json_file_path = f"{external_storage_path}/anime_list.json"

    json_data = []

    for anime_element in anime_list:
        img_element = anime_element.find('img')['src']
        img_url = img_element.split('?resize=')[0]
        anime = {
            "id": generate_random_id.generate_random_id(),
            "title": anime_element.find('div', class_='tt tts').find('h2').text,
            "slug": slugify(anime_element.find('div', class_='tt tts').find('h2').text, separator='-'),
            "type": anime_element.find('div', class_='typez').text,
            "status": anime_element.find('div', class_='bt').find('span', class_='epx').text,
            "img": img_url
        }

        json_data.append(anime)
    
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=2)
    
    print(f"Successfully save data to JSON file => {json_file_path}")

if __name__ == "__main__":
    main()