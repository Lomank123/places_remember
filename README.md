# Places Remember

## About this app
Places Remember - test project written with Django. It is a great opportunity to collect all wondrous moments in your life. Here you can mark places where you've been.

*This is my first fully constructed project with configured both frontend and backend. Help to improve it and let me know if there are any issues.*

**Stack:** Django + Postgres + Docker + Gunicorn + Heroku + Git + GitHub Actions

**Frontend:** React + Webpack + Leaflet + Babel

**Live working app link:** https://places-remember-app.herokuapp.com/home/

### Main features:
- **Create, delete and edit recollections**
  - Add marker on a map by clicking on location
  - Clicking on existing marker will delete it
  - There can be only 1 marker at a time
  - Observe all places you've added by clicking on recollections names on home page
- **Manage your profile**
  - You can change your email address, profile name, profile photo and password

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

In result there will be migrations applied, database will be filled with initial test data and also a superuser will be created:

Login: `admin`

Password: `12345`
```
docker-compose up filldb
```

**Run linters:**
```
docker-compose up lint
```