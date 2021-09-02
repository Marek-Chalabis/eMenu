# eMenu

> Web App for managing restaurants menus and dishes with REST API.

## Table of contents

- [General info](##general-info)
- [Features](#features)
- [Setup](#setup)
- [API documentation](#api-documentatin)
- [Tests](#tests)
- [Technologies](#technologies)
- [Contact](#contact)

## General info

The project aimed to create a Web App enabling the management of restaurants API.
Allows staff to create/modify menus by adding dishes. App sends email at 10 AM
to all Users with changed Dishes from last 24 hours. Also project provides custom
command to populate DB.

## Features

List of features:
- fully functional REST API
- optimized queries
- information about menus and dishes
- authorization system based on tokens
- clear line between public and protected endpoints
- custom actions
- scheduled emails
- custom command to populate DB with random data
- fully dockerized app

## Setup

1 Install Docker and Docker compose
2 Adjust environment variables in [.env](emenu/.env)
3 Build image (*all commands should be done in project root directory)
```
    docker-compose build
```
4 Run migrations
```
    docker-compose run --rm app ./manage.py migrate
```
5 Run containers
```
    docker-compose up
```
6 Optional - Populate DB with random data (add -h for help)
```
    docker-compose run --rm app ./manage.py populate_db_with_random_data
```

## Authorization

Easiest way for getting full access to app is to create superuser
by this command:
```
    docker-compose run --rm app ./manage.py createsuperuser
```
For token use this endpoint: `/api/v1/token-auth/`

Or create one from admin panel: `/admin/authtoken/tokenproxy/`

## API documentation

Documentation for API can found at this endpoints after running container:

- `/api/v1/documentation/` : Swagger documentation
- `/api/v1/` : Django Rest Framework Browsable API

## Tests

Flake8
```
    docker-compose run --rm app flake8
```

Pytest
```
    docker-compose run --rm app pytest -vv
```

Coverage
```
    docker-compose run --rm app pytest -vv --cov
```

## Technologies

- Python 
- Django 
- Django REST framework 
- Redis
- Celery
- [Python packages](requirements.txt)

## Contact

Created by <b>Marek Chałabis</b> email: chalabismarek@gmail.com
