import json

def url_request(depart_coord, arriv_coord):
    return 'http://router.project-osrm.org/route/v1/driving/'\
        f'{depart_coord[0]},{depart_coord[1]};{arriv_coord[0]},{arriv_coord[1]}?overview=false'

if __name__ == "__main__":
    with open('cities.json', 'r', encoding='utf8') as cities_json:
        cities_data = json.load(cities_json)
        print(cities_data)
