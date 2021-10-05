# places_remember
Places Remember - test project written with Django

Stack: Django + Postgres + Docker + Gunicorn + Heroku + Git

Frontend: React + Webpack + Leaflet + Babel

## Preparation

Assuming you have Docker installed on your PC at first you need to clone repository:
```
git clone https://github.com/Lomank123/places_remember.git
```

Then go to project root folder:
```
cd places_remember
```

Now very important thing: you need to copy content from `.env.sample` to `.env` file to use environment variables
The way you copy may vary, so I'll show how I did this on Windows 10:
```
copy .env.sample .env
```

## Building and running the app

**Build project:**

For the first time it may take 5-10 minutes to build everything (depends on your internet connection and PC hardware)
```
docker-compose up --build
```

**Launch project:**
```
docker-compose up placerem
```

**Run tests:**
```
docker-compose up test
```

**Fill db:**

In result there will be migrations applied, database will be filled with initial test data and also a superuser will be created: login: `admin`, password: `12345`
```
docker-compose up filldb
```

**Run linters:**
```
docker-compose up lint
```