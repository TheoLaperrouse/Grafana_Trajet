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
                    "`duration` DECIMAL(5,2) NOT NULL,"\
                    "`distance` DECIMAL(5,2) NOT NULL) ENGINE = InnoDB;"


def insert_route_infos(db_connex, cities_data):
    cities = cities_data['cities']
    config = dotenv_values('.env')
    for interest_point_key in cities_data['interest_points'].keys():
        lat, long = cities_data['interest_points'][interest_point_key]
        for city_key in cities.keys():

            lat_city, long_city = cities[city_key]
            now = datetime.now()
            route_data = requests.get(
                "https://maps.googleapis.com/maps/api/directions/json?"
                f"origin={long_city}%2C{lat_city}&destination={long}%2C{lat}"
                f"&departure_time={int(now.timestamp())}"
                f"&key={config['GOOGLE_DIRECTIONS_TOKEN']}",
                timeout=10).json()
            duration = route_data['routes'][0]["legs"][0]["duration_in_traffic"]['value']
            distance = route_data['routes'][0]["legs"][0]["distance"]['value']
            add_route_query = 'INSERT INTO `app_db`.`routes`' \
                '(date, departure, arrival, duration, distance) VALUES (' \
                f' "{now}",'\
                f'"{city_key}", "{interest_point_key}",'\
                f'"{duration}", "{distance}")'
            db_connexion.cursor().execute(add_route_query)
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
        time.sleep(900)
