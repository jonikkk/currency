import csv
import random
import re
import sqlite3
from time import sleep



import requests
from bs4 import BeautifulSoup

base_url = 'https://auto.ria.com'


def random_sleep():
    sleep(random.randint(2, 5))


def get_page_content(page: int, page_size: int = 100):
    query_params = {
        'indexName': 'auto,order_auto,newauto_search',
        'categories.main.id': '1',
        'country.import.usa.not': '-1',
        'price.currency': '1',
        'abroad.not': '0',
        'custom.not': '1',
        'page': page,
        'size': page_size,
    }
    url = f'{base_url}/uk/search/'

    response = requests.get(url, params=query_params)
    response.raise_for_status()
    return response.text


def get_detail_content(link: str):
    link = base_url + link
    print(link)
    response = requests.get(link)
    response.raise_for_status()
    return response


class CSVWriter:
    def __init__(self, file_name: str, headers: list):
        self.file_name = file_name

        with open(self.file_name, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

    def write_data(self, data):
        with open(self.file_name, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(data)


class StdoutWriter:
    def write_data(self, data):
        print(data)


class DBWriter:
    def __init__(self, db_name='auto_ria.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_id INTEGER NOT NULL,
                car_mark_details TEXT,
                car_model_name TEXT,
                car_year INTEGER,
                car_link_to_view TEXT,
                car_vin TEXT 
            )
        ''')
        self.conn.commit()

    def write_data(self, data):
        try:
            self.cursor.execute('''
                INSERT INTO cars (car_id, car_mark_details, car_model_name, car_year, car_link_to_view, car_vin)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', data)
            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()


def main():
    page = 0
    headers = ['id', 'mark', 'model', 'year', 'link', 'vin']

    writers = (
        CSVWriter('cars1.csv', headers),
        DBWriter(),
        # StdoutWriter(),
    )

    while True:
        random_sleep()
        print(f"Processing page {page}!")

        page_content = get_page_content(page)

        soup = BeautifulSoup(page_content, 'html.parser')
        search_results = soup.find('div', id="searchResults")
        ticket_items = search_results.find_all("section", class_="ticket-item")

        if not ticket_items:
            print(f"No more items on page {page}!")
            break

        pattern = r'vehicleIdentificationNumber":"([^"]*)"'

        for ticket_item in ticket_items:
            car_details = ticket_item.find("div", class_="hide")
            car_id = car_details['data-id']
            car_mark_details = car_details['data-mark-name']
            car_model_name = car_details['data-model-name']
            car_year = car_details['data-year']
            car_link_to_view = car_details['data-link-to-view']
            detail_content = get_detail_content(car_link_to_view)
            detail_soup = BeautifulSoup(detail_content.content, 'html.parser')
            context = detail_soup.find('script', id="ldJson2").text
            if match := re.search(pattern, context):
                car_vin = match[1]
            else:
                print("Value not found.")

            data = [car_id, car_mark_details, car_model_name, car_year, car_link_to_view, car_vin]

            for writer in writers:
                writer.write_data(data)

        page += 1


if __name__ == '__main__':
    main()
