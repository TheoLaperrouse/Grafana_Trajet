# Project

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

If you have some problems with rights on data folder :
```
sudo chown -R $USER data/db/app_db
```