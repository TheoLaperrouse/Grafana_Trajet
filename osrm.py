from datetime import datetime
import json
import time
import requests
import mysql.connector

ADD_ROUTE_QUERY = "INSERT INTO `app_db`.`routes`" \
    "(date, departure, arrival, duration)" \
    "VALUES (%s,%s,%s,%s)"
ROUTE_TABLE_QUERY = "CREATE TABLE IF NOT EXISTS `app_db`.`routes` ("\
                    "`date` INT NOT NULL ,"\
                    "`departure` INT NOT NULL ,"\
                    "`arrival` INT NOT NULL ,"\
                    "`duration` INT NOT NULL ) ENGINE = InnoDB;"


def insert_route_infos(cursor, cities_data):
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
            now = datetime.now().date()
            duration = round(route_data["routes"][0]["duration"]/60, 2)
            route_data = (now, city_key, interest_point_key, duration)
            cursor.execute(ADD_ROUTE_QUERY, route_data)


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
        insert_route_infos(database_cursor, cities_json)
        time.sleep(60)
