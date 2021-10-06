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
  - Sign up using VK or GitHub

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

**Stop project:**
```
docker-compose down
```

**Run tests:**
```
docker-compose up test
```

**Fill db:**

In result there will be migrations applied, database will be filled with initial test data and also a superuser will be created:

Login: `admin@gmail.com`

Password: `12345`

**Default users:**
  - Login: `test1@gmail.com` password: `12345678qQ`
  - Login: `test2@gmail.com` password: `12345678qQ`

```
docker-compose up filldb
```

**Run linters:**
```
docker-compose up lint
```

## Useful info

- If you want to use authentication with VK or GitHub you'll need to register new app and replace these environment variables in `.env` file:

**For VK:**
```
SOCIAL_AUTH_VK_OAUTH2_KEY=newkey
SOCIAL_AUTH_VK_OAUTH2_SECRET=newsecret
```

Tutorial link: https://vk.com/dev/vkapp_create

**For GitHub:**
```
SOCIAL_AUTH_GITHUB_KEY=newkey
SOCIAL_AUTH_GITHUB_SECRET=newsecret
```

Tutorial link: https://docs.github.com/en/developers/apps/building-github-apps/creating-a-github-app

- If you want to use Mapbox maps you'll need to provide it's token:

  - Get token (Docs: https://docs.mapbox.com/help/getting-started/access-tokens/)
  - Replace environment variable in `.env` file with your newly created token:
  ```
  MAP_ACCESS_TOKEN=newtoken
  ```

- If you want to use Dropbox storage you'll also need to enable it and provide it's token: 
  - To enable you need to change `USE_DROPBOX` environment variable in `.env` file:
  ```
  USE_DROPBOX=TRUE
  ```
  It should be set to `TRUE`, it's case-sensitive so any other values will cause using local storage at `/data`

  - Get token (Docs: https://www.dropbox.com/developers/documentation/python#tutorial)
  - Replace environment variable in `.env` file with your newly created token:
  ```
  DROPBOX_OAUTH2_TOKEN=newtoken
  ```