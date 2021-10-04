# places_remember
Places Remember - test project written with Django

Stack: Django + Postgres + Docker + Gunicorn + Heroku + Git

Frontend: React + Webpack + Leaflet + Babel


To launch project:
```
docker-compose up placerem
```

To run tests:
```
docker-compose up test
```

To fill db:
```
docker-compose up filldb
```
In result there're will be migrations applied, db will be filled with initial test data and also a superuser will be created: login: admin, password: 12345 

To launch linters:
```
docker-compose up lint
```