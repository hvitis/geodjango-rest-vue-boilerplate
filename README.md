# GeoDjango REST Vue Boilerplate 💚🐍
___
![Vue Logo](./src/assets/main-logo.png "Vue Logo")

This template is a boilerplate to explain geodjango with front-end implementation. 

### Demo

[Live Demo](https://geodjango-rest-vue-boilerplate.herokuapp.com/)

### Includes

* Django
* Django REST framework
* Django Whitenoise, CDN Ready
* Vue CLI 3
* Vue Router
* Vuex
* Gunicorn
* Configuration for Heroku Deployment


### Examples


| Components             |  Content                                   |
|----------------------|--------------------------------------------|
| `/map`           | Leaflet Map          |
| `/address`       | Searching via address                        |


## Prerequisites

Before getting started you should have the following installed and running:

- [X] Yarn - [instructions](https://yarnpkg.com/en/docs/install)
- [X] Vue CLI 3 - [instructions](https://cli.vuejs.org/guide/installation.html)
- [X] Python 3 - [instructions](https://wiki.python.org/moin/BeginnersGuide)
- [X] Pipenv - [instructions](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv)

## Setup Template

```
$ git clone https://github.com/gtalarico/django-vue-template
$ cd django-vue-template
```

Setup
```
$ yarn install
$ pip install -r requirements.txt
$ python manage.py migrate
```

## Running Development Servers

1. Create .env file with your geodatabase credentials:
(geospatial database is just PostgreSQL database with postgis extension)
```
DB_NAME=YOUR_DB_NAME
DB_USER=YOUR_DB_USER
DB_PASSWORD=YOUR_PASSWORD
```

```
$ python manage.py runserver
```

From another tab in the same directory:

```
$ yarn serve
```

The Vue application will be served from [`localhost:8080`](http://localhost:8080/) and the Django API
and static files will be served from [`localhost:8000`](http://localhost:8000/).


## Deploy

* Set `ALLOWED_HOSTS` on [`backend.settings.prod`](/backend/settings/prod.py)

### Heroku Server

```
$ heroku apps:create django-vue-template-demo
$ heroku git:remote --app django-vue-template-demo
$ heroku buildpacks:add --index 1 heroku/nodejs
$ heroku buildpacks:add --index 2 heroku/python
$ heroku addons:create heroku-postgresql:hobby-dev
$ heroku config:set DJANGO_SETTINGS_MODULE=backend.settings.prod
$ heroku config:set DJANGO_SECRET_KEY='...(your django SECRET_KEY value)...'

$ git push heroku
```

##### Heroku One Click Deploy

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/hvitis/geodjango-rest-vue-boilerplate)

#### Thanks

I build it using [django-vue-template][0]. Check it out for more information.


[0]: https://github.com/gtalarico/django-vue-template