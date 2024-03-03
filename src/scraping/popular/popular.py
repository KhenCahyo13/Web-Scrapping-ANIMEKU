from bs4 import BeautifulSoup
from dotenv import load_dotenv
import sys
import os
import requests
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'helpers')))

import generate_random_id

load_dotenv()
base_url = os.getenv('ANIMEKU_BASE_URL')
external_storage_path = os.getenv('EXTERNAL_STORAGE_PATH')

def main() :
    iterate_popular_anime()

def scrap_popular_anime():
    try:
        animeku_request = requests.get(base_url)
        animeku_request.raise_for_status()
        soup = BeautifulSoup(animeku_request.text, 'lxml')

        weekly_popular = soup.find('div', class_='wpop-weekly').find('ul').find_all('li')
        monthly_popular = soup.find('div', class_='wpop-monthly').find('ul').find_all('li')
        alltime_popular = soup.find('div', class_='wpop-alltime').find('ul').find_all('li')

        return {
            'weekly_popular': weekly_popular,
            'monthly_popular': monthly_popular,
            'alltime_popular': alltime_popular
        }
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def iterate_popular_anime():
    popular_anime_data = scrap_popular_anime()
    json_file_path = f"{external_storage_path}/anime_popular.json"

    json_data = {
        'weekly_popular': [],
        'monthly_popular': [],
        'alltime_popular': []
    }

    for key, anime_list in popular_anime_data.items():
        for anime_element in anime_list:
            genre_list = []
            genres = anime_element.find('span').find_all('a')

            for genre in genres:
                genre_list.append(genre.text)

            img_element = anime_element.find('div', class_='imgseries').find('a').find('img')['src']
            img_url = img_element.split('?resize=')[0]
            anime = {
                "id": generate_random_id.generate_random_id(),
                "title": anime_element.find('h4').find('a').text,
                "genres": genre_list,
                "rating": anime_element.find('div', class_='rt').find('div', class_='numscore').text,
                "img": img_url
            }

            json_data[key].append(anime)

    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=2)
    
    print(f"Successfully save data to JSON file => {json_file_path}")

if __name__ == "__main__":
    main()