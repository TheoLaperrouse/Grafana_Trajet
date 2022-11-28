import json
import requests

cities = [
          "Thorigné-Fouillard",
          "Combourg",
          "Saint Aubin d'Aubigné", "Liffré", "Saint Aubin du Cormier",
          "Feins", "Bonnemain","Val Couesnon",
          "Pontorson", "La Mézière"
        ]

cities_data = {
                "interest_points": {
                    "TFTT": [-1.5766265,48.1523132],
                    "Parking Mont Saint Michel": [-1.5066622,48.6117652],
                    "Energiency": [-1.7015696,48.0984544],
                },
                "cities":{}
            }

if __name__ == '__main__':
    for city in cities:
        city_data = requests.get(
            f"https://geo.api.gouv.fr/communes/?nom={city}&fields=nom,mairie", timeout=10).json()[0]
        cities_data['cities'][city_data['nom']] = city_data['mairie']['coordinates']
    with open('cities.json', 'w', encoding='utf8') as f:
        json.dump(cities_data, f, ensure_ascii=False, sort_keys=True, indent=4)
