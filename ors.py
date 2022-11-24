from datetime import datetime
import json
import time
import requests
import mysql.connector
from dotenv import load_dotenv, dotenv_values

load_dotenv()

ROUTE_TABLE_QUERY = "CREATE TABLE IF NOT EXISTS `app_db`.`routes` ("\
                    "`date` VARCHAR(40) NOT NULL ,"\
                    "`departure` VARCHAR(40) NOT NULL ,"\
                    "`arrival` VARCHAR(40) NOT NULL ,"\
                    "`duration` DECIMAL(5) NOT NULL ) ENGINE = InnoDB;"


def insert_route_infos(db_connex, cities_data):
    cursor = db_connexion.cursor()
    interest_points = cities_data['interest_points']
    cities = cities_data['cities']
    config = dotenv_values('.env')
    for interest_point_key in interest_points.keys():
        lat, long = interest_points[interest_point_key]
        for city_key in cities.keys():
            lat_city, long_city = cities[city_key]
            route_data = requests.get(
                'https://api.openrouteservice.org/v2/directions/driving-car?'\
                f'api_key={config["ORS_TOKEN"]}'\
                f'&start={lat_city},{long_city}&end={lat},{long}',
                timeout=10).json()
            duration = round(route_data['features'][0]["properties"]["summary"]['duration']/60, 2)
            add_route_query = 'INSERT INTO `app_db`.`routes`' \
                        '(date, departure, arrival, duration) VALUES (' \
                        f' "{datetime.now().isoformat()}",'\
                        f'"{city_key}", "{interest_point_key}", "{duration}")'
            cursor.execute(add_route_query)
    db_connex.commit()


if __name__ == "__main__":
    db_connexion = mysql.connector.connect(
        host='db',
        user='db_user',
        password='db_user_pass',
        port=3306
    )
    database_cursor = db_connexion.cursor()
    database_cursor.execute(ROUTE_TABLE_QUERY)
    with open('cities.json', 'r', encoding='utf8') as f:
        cities_json = json.load(f)
    while True:
        insert_route_infos(db_connexion, cities_json)
        time.sleep(1800)
