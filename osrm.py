from datetime import datetime
import json
import time
import requests
import mysql.connector

ROUTE_TABLE_QUERY = "CREATE TABLE IF NOT EXISTS `app_db`.`routes` ("\
                    "`date` VARCHAR(40) NOT NULL ,"\
                    "`departure` VARCHAR(40) NOT NULL ,"\
                    "`arrival` VARCHAR(40) NOT NULL ,"\
                    "`duration` DECIMAL(5) NOT NULL ) ENGINE = InnoDB;"


def insert_route_infos(db_connex, cities_data):
    cursor = db_connexion.cursor()
    interest_points = cities_data['interest_points']
    cities = cities_data['cities']
    for interest_point_key in interest_points.keys():
        lat, long = interest_points[interest_point_key]
        for city_key in cities.keys():
            lat_city, long_city = cities[city_key]
            route_data = requests.get(
                'http://router.project-osrm.org/route/v1/car/'
                f'{lat},{long};{lat_city},{long_city}',
                timeout=10).json()
            now = datetime.now().isoformat()
            duration = round(route_data["routes"][0]["duration"]/60, 2)
            add_route_query = 'INSERT INTO `app_db`.`routes`' \
                        '(date, departure, arrival, duration)' \
                        f' VALUES ("{now}", "{city_key}", "{interest_point_key}", "{duration}")'
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
        time.sleep(3600)
