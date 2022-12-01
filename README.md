# Project

Utilisation de l'api Google Directions pour récupérer les différents temps de trajets entre deux destinations, les enregistrer en base de données (MySQL), puis afficher les valeurs à l'aide de Grafana.

![grafana](https://user-images.githubusercontent.com/31164468/205183207-4636e145-8073-4b52-a12a-40af31e47246.jpg)

## Développement

Utilisation de pylint et de precommit :

```sh

pre-commit install
```
```sh
pylint **/*.py
```

To get ready :
- Get a token for the API of GoogleMaps
- Add it to the associated env variable in .env

## Fonctionnement

Pour effectuer des calculs de trajets selon les différentes heures de la journée

Enregistrement des données en BDD sur container en local (données persistantes dans /data/db)

Construction de l'image Docker : 
```sh
docker-compose up --build
```
Problèmes de droits sur le dossier data/db/app_db :
```
sudo chown -R $USER data/db/app_db
```



