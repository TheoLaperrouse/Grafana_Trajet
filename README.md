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
- Get a token for the API of ORS : https://openrouteservice.org/dev/#/api-docs/v2/directions/{profile}/get
- Add it to the associated env variable in .env

## Fonctionnement

Utilisation de l'API open source : https://project-osrm.org/docs/v5.24.0/api/#

Pour effectuer des calculs de trajets selon les différentes heures de la journée

Enregistrement des données en BDD sur container en local

Construction de l'image Docker : 
```sh
docker build -t orsApp .
```